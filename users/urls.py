from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import (
    UserRegisterView,
    UserProfileView,
    UserUpdateView,
    UserListView,
    UserDeleteView, PasswordResetView, PasswordResetConfirmView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name='profile-update'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Логин
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Обновление токена

    path('reset_password/', PasswordResetView.as_view(), name='reset_password'), # <--- Добавь это
    path('reset_password_confirm/', PasswordResetConfirmView.as_view(), name='reset_password_confirm'), # <--- И это
]