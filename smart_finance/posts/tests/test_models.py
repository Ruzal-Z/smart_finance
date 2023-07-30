"""Тест моделей приложения посты"""
from django.test import TestCase
from posts.models import (COMMENT, FOLLOW, POST, Comment, Follow, Group, Post,
                          User)


class PostModelTest(TestCase):
    """Класс для тестирования"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username="author")
        cls.follower = User.objects.create_user(username="followerone")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="Тестовый слаг",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            group=cls.group,
            author=cls.user,
            text="Тестовый длинный пост, очень длинный",
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Мой тестовый комментарий',
        )
        cls.follow = Follow.objects.create(
            user=cls.follower,
            author=cls.user,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        cases = [
            (
                POST.format(
                    self.post.author.username,
                    self.post.group,
                    self.post.pub_date,
                    self.post.text,
                ),
                self.post,
            ),
            (self.group.title, self.group),
            (
                COMMENT.format(
                    self.comment.author.username, self.comment.text
                ),
                self.comment,
            ),
            (
                FOLLOW.format(
                    self.follow.user.username, self.follow.author.username
                ),
                self.follow,
            ),
        ]
        for expected_value, resulting_value in cases:
            with self.subTest(
                expected_value=expected_value, resulting_value=resulting_value
            ):
                self.assertEqual(expected_value, str(resulting_value))
