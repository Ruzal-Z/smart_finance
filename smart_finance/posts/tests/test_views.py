import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Follow, Group, Post, User

USER_NAME = 'UserAuthor'
OTHER_USER_NAME = 'UserAuthorized'
GROUP_SLUG = 'test-slug'
OTHER_GROUP_SLUG = 'other-slug'

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

POSTS_SECOND_PAGE: int = 5
INDEX_URL = reverse('posts:index')
GROUP_LIST_URL = reverse('posts:group_list', args=[GROUP_SLUG])
GROUP_LIST_URL_OTHER = reverse('posts:group_list', args=[OTHER_GROUP_SLUG])
PROFILE_URL = reverse('posts:profile', args=[USER_NAME])
FOLLOW_INDEX_URL = reverse('posts:follow_index')
PROFILE_FOLLOW_URL = reverse('posts:profile_follow', args=[USER_NAME])
PROFILE_UNFOLLOW_URL = reverse('posts:profile_unfollow', args=[USER_NAME])
FOLLOW_INDEX_URL = reverse('posts:follow_index')
SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(USER_NAME)
        cls.other_user = User.objects.create_user(OTHER_USER_NAME)
        cls.guest = Client()
        cls.author = Client()
        cls.author.force_login(cls.user)
        cls.another = Client()
        cls.another.force_login(cls.other_user)

        cls.uploaded = SimpleUploadedFile(
            name='small.gif', content=SMALL_GIF, content_type='image/gif'
        )
        cls.group = Group.objects.create(
            title='Тестовая гурппа',
            description='Тестовое описание',
            slug=GROUP_SLUG,
        )
        cls.group_other = Group.objects.create(
            title='Тестовый заголовок другой группы',
            description='Тестовое описание др.гр.',
            slug=OTHER_GROUP_SLUG,
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
            image=cls.uploaded,
        )
        cls.follow = Follow.objects.create(
            user=cls.other_user,
            author=cls.user,
        )
        cls.POST_DETAIL_URL = reverse('posts:post_detail', args=[cls.post.pk])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()

    def test_paginator(self):
        """Тестирование Paginator."""
        Post.objects.all().delete()
        cache.clear()
        Post.objects.bulk_create(
            Post(
                author=self.user,
                text=f'Тестовый пост номер {i}',
                group=self.group,
            )
            for i in range(settings.COUNT_POST + POSTS_SECOND_PAGE)
        )
        elements = (
            (INDEX_URL, settings.COUNT_POST, self.author),
            (INDEX_URL + '?page=2', POSTS_SECOND_PAGE, self.author),
            (GROUP_LIST_URL, settings.COUNT_POST, self.author),
            (GROUP_LIST_URL + '?page=2', POSTS_SECOND_PAGE, self.author),
            (PROFILE_URL, settings.COUNT_POST, self.author),
            (PROFILE_URL + '?page=2', POSTS_SECOND_PAGE, self.author),
            (FOLLOW_INDEX_URL, settings.COUNT_POST, self.another),
            (
                FOLLOW_INDEX_URL + '?page=2',
                POSTS_SECOND_PAGE,
                self.another,
            ),
        )

        for page_url, post_count, client in elements:
            with self.subTest(page_url=page_url):
                self.assertEqual(
                    len(client.get(page_url).context['page_obj']),
                    post_count,
                )

    def test_context_page(self):
        """Тест контекста"""
        urls_for_clients = [
            (INDEX_URL, self.author),
            (GROUP_LIST_URL, self.author),
            (PROFILE_URL, self.author),
            (self.POST_DETAIL_URL, self.author),
            (FOLLOW_INDEX_URL, self.another),
        ]
        for url, client in urls_for_clients:
            with self.subTest(url=url):
                response = client.get(url)
                if 'page_obj' in response.context:
                    self.assertEqual(len(response.context['page_obj']), 1)
                    post = response.context['page_obj'][0]
                else:
                    post = response.context['post']
                self.assertEqual(post.pk, self.post.pk)
                self.assertEqual(post.text, self.post.text)
                self.assertEqual(post.author, self.post.author)
                self.assertEqual(post.group, self.post.group)
                self.assertEqual(post.image, self.post.image)

    def test_group_correct_context(self):
        """Тест контекста group_posts."""
        group = self.guest.get(GROUP_LIST_URL).context.get('group')
        self.assertEqual(group.pk, self.group.pk)
        self.assertEqual(group.title, self.group.title)
        self.assertEqual(group.description, self.group.description)
        self.assertEqual(group.slug, self.group.slug)

    def test_profile_correct_context(self):
        """Тест контекста profile."""
        self.assertEqual(
            self.guest.get(PROFILE_URL).context.get('author'),
            self.user,
        )

    def test_post_doesnt_appear_in_wrong_pages(self):
        urls_list = [GROUP_LIST_URL_OTHER, FOLLOW_INDEX_URL]
        for url in urls_list:
            self.assertNotIn(
                self.post, self.author.get(url).context['page_obj']
            )

    def test_cache_index(self):
        page_view = self.author.get(INDEX_URL).content
        Post.objects.all().delete()
        page_view_cache = self.author.get(INDEX_URL).content
        self.assertEqual(page_view, page_view_cache)
        cache.clear()
        page_view__clear = self.author.get(INDEX_URL).content
        self.assertNotEqual(page_view, page_view__clear)

    def test_auth_user_follow(self):
        """Авторизованный пользователь может подписаться"""
        Follow.objects.all().delete()
        self.another.get(PROFILE_FOLLOW_URL)
        self.assertEqual(Follow.objects.count(), 1)
        self.assertTrue(
            Follow.objects.filter(
                author=self.user, user=self.other_user
            ).exists()
        )

    def test_auth_user_unfollow(self):
        """Авторизованный пользователь может отписатся"""
        Follow.objects.all().delete()
        Follow.objects.create(user=self.other_user, author=self.user)
        self.another.get(PROFILE_UNFOLLOW_URL)
        self.assertFalse(
            Follow.objects.filter(
                author=self.user, user=self.other_user
            ).exists()
        )
