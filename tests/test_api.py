import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from ads.models import Ad, Review
from users.models import User


@pytest.mark.django_db
def test_user_registration():
    """Тест: регистрация нового пользователя"""
    client = APIClient()
    url = reverse("register")
    data = {"email": "newuser@example.com", "password": "StrongPass123", "first_name": "New", "last_name": "User"}
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert User.objects.filter(email="newuser@example.com").exists()


@pytest.mark.django_db
def test_create_ad_authenticated():
    """Тест: авторизованный пользователь может создать объявление"""
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", username="user", password="password123")
    client.force_authenticate(user=user)

    url = reverse("ad-list-create")
    data = {"title": "Мое объявление", "price": 1000, "description": "Тест"}
    response = client.post(url, data, format="json")

    assert response.status_code == 201
    assert Ad.objects.count() == 1


@pytest.mark.django_db
def test_create_ad_anonymous():
    """Тест: анонимный пользователь не может создать объявление"""
    client = APIClient()
    url = reverse("ad-list-create")
    data = {"title": "Чужое", "price": 500}
    response = client.post(url, data, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_ad_search():
    """Тест: поиск объявлений по названию"""
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", username="user", password="password123")

    Ad.objects.create(title="Тестовое объявление", price=100, author=user)
    Ad.objects.create(title="Другое", price=200, author=user)

    url = reverse("ad-list-create") + "?search=Тестовое"
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["title"] == "Тестовое объявление"


@pytest.mark.django_db
def test_edit_other_ad_forbidden():
    """Тест: пользователь не может редактировать чужое объявление"""
    client = APIClient()

    author = User.objects.create_user(email="author@example.com", username="author", password="password123")
    other_user = User.objects.create_user(email="other@example.com", username="other", password="password123")

    ad = Ad.objects.create(title="Оригинал", price=100, author=author)

    client.force_authenticate(user=other_user)

    url = reverse("ad-detail", args=[ad.id])
    data = {"title": "Взлом"}
    response = client.patch(url, data, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_review():
    """Тест: создание отзыва к объявлению"""
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", username="user", password="password123")
    ad = Ad.objects.create(title="Товар", price=100, author=user)

    client.force_authenticate(user=user)

    url = reverse("review-list-create")
    data = {"text": "Отличный товар!", "ad": ad.id}
    response = client.post(url, data, format="json")

    assert response.status_code == 201
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_edit_own_ad():
    """Тест: пользователь может редактировать СВОЕ объявление"""
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", username="user", password="password123")
    ad = Ad.objects.create(title="Оригинал", price=100, author=user)

    client.force_authenticate(user=user)
    url = reverse("ad-detail", args=[ad.id])
    data = {"title": "Изменено"}
    response = client.patch(url, data, format="json")

    assert response.status_code == 200
    ad.refresh_from_db()
    assert ad.title == "Изменено"


@pytest.mark.django_db
def test_delete_own_ad():
    """Тест: пользователь может удалить СВОЕ объявление"""
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", username="user", password="password123")
    ad = Ad.objects.create(title="Удаляемое", price=100, author=user)

    client.force_authenticate(user=user)
    url = reverse("ad-detail", args=[ad.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert not Ad.objects.filter(id=ad.id).exists()


@pytest.mark.django_db
def test_pagination():
    """Тест: пагинация (не более 4 объектов на странице)"""
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", username="user", password="password123")

    for i in range(5):
        Ad.objects.create(title=f"Объявление {i}", price=100, author=user)

    url = reverse("ad-list-create")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data["results"]) == 4
    assert response.data["count"] == 5


@pytest.mark.django_db
def test_edit_own_review():
    """Тест: пользователь может редактировать свой отзыв"""
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", username="user", password="password123")
    ad = Ad.objects.create(title="Товар", price=100, author=user)
    review = Review.objects.create(text="Старый отзыв", ad=ad, author=user)

    client.force_authenticate(user=user)
    url = reverse("review-detail", args=[review.id])
    data = {"text": "Новый отзыв"}
    response = client.patch(url, data, format="json")

    assert response.status_code == 200
    review.refresh_from_db()
    assert review.text == "Новый отзыв"


@pytest.mark.django_db
def test_token_obtain():
    """Тест: получение JWT-токена (логин)"""
    client = APIClient()
    User.objects.create_user(email="user@example.com", username="user", password="password123")

    url = reverse("token_obtain_pair")
    data = {"email": "user@example.com", "password": "password123"}
    response = client.post(url, data, format="json")

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_password_reset_request(mailoutbox):
    """Тест: запрос на сброс пароля (проверяем, что письмо отправляется)"""
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", username="user", password="password123")

    url = reverse("reset_password")
    data = {"email": "user@example.com"}
    response = client.post(url, data, format="json")

    assert response.status_code == 200
    assert len(mailoutbox) == 1
    assert "Восстановление пароля" in mailoutbox[0].subject
    assert user.email in mailoutbox[0].to


@pytest.mark.django_db
def test_password_reset_confirm():
    """Тест: подтверждение сброса пароля (смена пароля)"""
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", username="user", password="password123")

    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    url = reverse("reset_password_confirm")
    data = {"uid": uid, "token": token, "new_password": "NewStrongPass123"}
    response = client.post(url, data, format="json")

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password("NewStrongPass123")


@pytest.mark.django_db
def test_profile_update():
    """Тест: пользователь может обновить свой профиль"""
    client = APIClient()
    user = User.objects.create_user(email="user@example.com", username="user", password="password123")
    client.force_authenticate(user=user)

    url = reverse("profile-update")
    data = {"first_name": "НовоеИмя"}
    response = client.patch(url, data, format="json")

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.first_name == "НовоеИмя"


@pytest.mark.django_db
def test_user_delete():
    """Тест: удаление пользователя"""
    client = APIClient()
    admin = User.objects.create_superuser(email="admin@example.com", username="admin", password="adminpass")
    user_to_delete = User.objects.create_user(email="delete@example.com", username="delete", password="password123")

    client.force_authenticate(user=admin)
    url = reverse("user-delete", args=[user_to_delete.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert not User.objects.filter(id=user_to_delete.id).exists()


@pytest.mark.django_db
def test_delete_other_review_forbidden():
    """Тест: пользователь не может удалить чужой отзыв"""
    client = APIClient()
    author = User.objects.create_user(email="author@example.com", username="author", password="password123")
    other_user = User.objects.create_user(email="other@example.com", username="other", password="password123")

    ad = Ad.objects.create(title="Товар", price=100, author=author)
    review = Review.objects.create(text="Отзыв", ad=ad, author=author)

    client.force_authenticate(user=other_user)
    url = reverse("review-detail", args=[review.id])
    response = client.delete(url)

    assert response.status_code == 403
