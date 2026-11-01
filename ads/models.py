from django.db import models
from django.conf import settings


class Ad(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название товара")
    price = models.PositiveIntegerField(verbose_name="Цена товара")
    description = models.TextField(verbose_name="Описание товара", blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        # Сортировка по дате создания: чем новее, тем выше
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Автор отзыва"
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Объявление"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        # Сортировка отзывов (обычно тоже новые сверху)
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.author.email} на {self.ad.title}"
