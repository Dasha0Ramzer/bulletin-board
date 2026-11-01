from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from users.models import User

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from users.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    PasswordResetSerializer,       # <--- Добавь
    PasswordResetConfirmSerializer # <--- Добавь
)


# 1. РЕГИСТРАЦИЯ (Создание пользователя)
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny] # Разрешаем доступ без токена

# 2. ПРОСМОТР ПРОФИЛЯ (Своего)
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Возвращаем профиль того пользователя, чей токен передан
        return self.request.user

# 3. РЕДАКТИРОВАНИЕ ПРОФИЛЯ
class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# 4. СПИСОК ВСЕХ ПОЛЬЗОВАТЕЛЕЙ (Для админа или общего просмотра)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# 5. УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ (Обычно только для админа)
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# 6. СБРОС ПАРОЛЯ (Запрос на почту)
class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Из соображений безопасности не раскрываем, есть ли такой email
            return Response({"detail": "Если пользователь существует, письмо отправлено."}, status=status.HTTP_200_OK)

        # 1. Шифруем ID пользователя (например, id=5 станет "NQ")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # 2. Генерируем секретный токен, привязанный к пользователю
        token = default_token_generator.make_token(user)

        # 3. Формируем ссылку, как в задании: /<url>/{uid}/{token}/
        reset_link = f"http://localhost:8000/users/reset_password_confirm/{uid}/{token}/"

        send_mail(
            subject='Восстановление пароля',
            message=f'Для сброса пароля перейдите по ссылке: {reset_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"detail": "Письмо отправлено."}, status=status.HTTP_200_OK)


# 7. ПОДТВЕРЖДЕНИЕ СБРОСА (Смена пароля)
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            # 1. Расшифровываем uid обратно в id
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Неверный uid"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Проверяем, что токен валиден (не истек и подходит к этому юзеру)
        if not default_token_generator.check_token(user, token):
            return Response({"error": "Неверный или истекший токен"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Меняем пароль
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK)


