from django.db import models


class Blog(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок статьи"
    )
    content = models.TextField(
        verbose_name="Содержание статьи"
    )
    image = models.ImageField(
        verbose_name="Изображение статьи",
        upload_to="blog/"
    )
    count_of_views = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="Количество просмотров"
    )
    publieshed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
