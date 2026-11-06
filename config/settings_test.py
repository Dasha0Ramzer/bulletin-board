from .settings import *

# Переопределяем базу данных для тестов
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DATABASE_NAME", "bulletin_board"),
        "USER": os.getenv("DATABASE_USER", "postgres"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "4588"), # <--- Вставь свой пароль
        "HOST": "localhost", # <--- ВОТ ГЛАВНОЕ ИЗМЕНЕНИЕ
        "PORT": "5432",
    }
}