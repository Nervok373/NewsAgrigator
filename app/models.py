from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

class News(models.Model):
    title = models.TextField("Название новости")
    author = models.CharField("Автор", max_length=30, default='Anon')
    time = models.TextField("Время публикации")
    description = models.TextField("Описание")
    link = models.TextField("Ссылка на статью")
    source = models.TextField("Источник новости")
    count_comments = models.TextField("Количество комментариев")
    news_id = models.TextField("ID новости на исходном сайте")
    score = models.TextField("Рейтинг новости но исходном сайте")

    def get_absolute_url(self):
        return self.link

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['time']
