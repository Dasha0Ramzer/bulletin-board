# 1. Берем официальный образ Python 3.14 (тонкую версию)
FROM python:3.14-slim

# 2. Отключаем буферизацию вывода (чтобы логи сразу шли в консоль) и создаем .pyc файлы (для скорости)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Создаем рабочую папку внутри контейнера
WORKDIR /app

# 4. Устанавливаем Poetry (так как у тебя зависимости через него)
RUN pip install --no-cache-dir poetry

# 5. Копируем файлы с зависимостями и устанавливаем их
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root

# 6. Копируем весь остальной код в контейнер
COPY . .

# 7. Открываем порт 8000 (на нем будет работать Django)
EXPOSE 8000

# 8. Команда запуска (сервер Django)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]