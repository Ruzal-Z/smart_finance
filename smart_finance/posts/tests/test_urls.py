from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User

USER_AUTHORIZED_AUTHOR = 'UserAuthor'
USER_AUTHORIZED = 'UserAuthorized'
SLUG = 'test-slug'

INDEX_URL = reverse('posts:index')
GROUP_LIST_URL = reverse('posts:group_list', args=[SLUG])
PROFILE_URL = reverse('posts:profile', args=[USER_AUTHORIZED_AUTHOR])
POST_CREATE_URL = reverse('posts:post_create')
LOGIN_URL = reverse('users:login')
REDIRECT_POST_CREATE_URL = f'{LOGIN_URL}?next={POST_CREATE_URL}'
FOLLOW_INDEX_URL = reverse('posts:follow_index')
FOLLOW_URL = reverse('posts:profile_follow', args=[USER_AUTHORIZED_AUTHOR])
UNFOLLOW_URL = reverse('posts:profile_unfollow', args=[USER_AUTHORIZED_AUTHOR])
REDIRECT_FOLLOW_URL = f'{LOGIN_URL}?next={FOLLOW_URL}'
REDIRECT_UNFOLLOW_URL = f'{LOGIN_URL}?next={UNFOLLOW_URL}'


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username=USER_AUTHORIZED_AUTHOR)
        cls.other_user = User.objects.create_user(username=USER_AUTHORIZED)
        cls.guest = Client()
        cls.author = Client()
        cls.author.force_login(cls.user)
        cls.another = Client()
        cls.another.force_login(cls.other_user)
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug=SLUG,
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )

        cls.POST_DETAIL_URL = reverse('posts:post_detail', args=[cls.post.pk])
        cls.POST_EDIT_URL = reverse('posts:post_edit', args=[cls.post.pk])
        cls.REDIRECT_POST_EDIT_URL = f'{LOGIN_URL}?next={cls.POST_EDIT_URL}'
        cls.ADD_COMMENT_URL = reverse('posts:add_comment', args=[cls.post.pk])

    def test_urls(self):
        url_and_clients = [
            (INDEX_URL, self.guest, 200),
            (GROUP_LIST_URL, self.guest, 200),
            (PROFILE_URL, self.guest, 200),
            (self.POST_DETAIL_URL, self.guest, 200),
            (POST_CREATE_URL, self.guest, 302),
            (self.POST_EDIT_URL, self.guest, 302),
            ('/unexisting_page/', self.guest, 404),
            (POST_CREATE_URL, self.author, 200),
            (self.POST_EDIT_URL, self.author, 200),
            (self.POST_EDIT_URL, self.another, 302),
            (self.ADD_COMMENT_URL, self.another, 302),
            (FOLLOW_INDEX_URL, self.guest, 302),
            (FOLLOW_INDEX_URL, self.another, 200),
            (FOLLOW_URL, self.guest, 302),
            (FOLLOW_URL, self.author, 302),
            (FOLLOW_URL, self.another, 302),
            (UNFOLLOW_URL, self.guest, 302),
            (UNFOLLOW_URL, self.author, 404),
            (UNFOLLOW_URL, self.another, 302),
        ]
        for address, client, status in url_and_clients:
            with self.subTest(address=address, client=client, status=status):
                self.assertEqual(client.get(address).status_code, status)

    def test_pages_uses_correct_template(self):
        templates_page_names = [
            (INDEX_URL, 'posts/index.html'),
            (GROUP_LIST_URL, 'posts/group_list.html'),
            (PROFILE_URL, 'posts/profile.html'),
            (self.POST_DETAIL_URL, 'posts/post_detail.html'),
            (POST_CREATE_URL, 'posts/create_post.html'),
            (self.POST_EDIT_URL, 'posts/create_post.html'),
            (FOLLOW_INDEX_URL, 'posts/follow.html'),
        ]

        for url, template in templates_page_names:
            with self.subTest(url=url):
                self.assertTemplateUsed(self.author.get(url), template)

    def test_redirect(self):
        cases = [
            (POST_CREATE_URL, REDIRECT_POST_CREATE_URL, self.guest),
            (self.POST_EDIT_URL, self.REDIRECT_POST_EDIT_URL, self.guest),
            (self.POST_EDIT_URL, self.POST_DETAIL_URL, self.another),
            (self.ADD_COMMENT_URL, self.POST_DETAIL_URL, self.another),
            (FOLLOW_URL, REDIRECT_FOLLOW_URL, self.guest),
            (FOLLOW_URL, PROFILE_URL, self.author),
            (FOLLOW_URL, PROFILE_URL, self.another),
            (UNFOLLOW_URL, REDIRECT_UNFOLLOW_URL, self.guest),
            (UNFOLLOW_URL, PROFILE_URL, self.another),
        ]
        for url, redirect, client in cases:
            with self.subTest(url=url, client=client):
                self.assertRedirects(
                    client.get(url),
                    redirect,
                )
