"""Создание моделей"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q

User = get_user_model()

POST = 'Автор: {}> Группа: {}> Дата публикации: {}> Текст: {:.15}'
COMMENT = 'Автор: {}> Текст: {:.15}'
FOLLOW = '{} подписан на {}'


class Group(models.Model):
    """Модель Group"""

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(
        unique=True, max_length=30, verbose_name='Идентификатор'
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Модель Post"""

    text = models.TextField(
        verbose_name='Текст поста', help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикаций'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост',
    )
    image = models.ImageField(
        'Картинка',
        upload_to=settings.UPLOAD_PATH,
        blank=True,
        help_text='Загрузите картинку',
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return POST.format(
            self.author.username, self.group, self.pub_date, self.text
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        'Текст комментария', help_text='Текст нового комментария'
    )
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return COMMENT.format(self.author.username, self.text)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='unique_follow', fields=['author', 'user']
            ),
            models.CheckConstraint(
                name='not_follow', check=~Q(user=F('author'))
            ),
        ]

    def __str__(self):
        return FOLLOW.format(self.user.username, self.author.username)
