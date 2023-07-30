import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Comment, Group, Post, User

USER_NAME = 'TestUser'
OTHER_USER_NAME = 'TestUser1'
GROUP_SLUG = 'test-slug'
UPLOAD_PATH = settings.UPLOAD_PATH

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

PROFILE_URL = reverse('posts:profile', args=[USER_NAME])
POST_CREATE_URL = reverse('posts:post_create')
LOGIN = reverse('users:login')
REDIRECT_LOGIN_URL = f'{LOGIN}?next={POST_CREATE_URL}'
SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)


def get_uploaded(image_name='test_pic.gif'):
    return SimpleUploadedFile(
        name=image_name,
        content=SMALL_GIF,
        content_type='image/gif',
    )


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username=USER_NAME)
        cls.other_user = User.objects.create_user(username=OTHER_USER_NAME)
        cls.guest = Client()
        cls.author = Client()
        cls.author.force_login(cls.user)
        cls.another = Client()
        cls.another.force_login(cls.other_user)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug=GROUP_SLUG,
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )

        cls.POST_DETAIL_URL = reverse('posts:post_detail', args=[cls.post.pk])
        cls.POST_EDIT_URL = reverse('posts:post_edit', args=[cls.post.pk])
        cls.REDIRECT_URL_LOGIN_EDIT = f'{LOGIN}?next={cls.POST_EDIT_URL}'
        cls.ADD_COMMENT_URL = reverse('posts:add_comment', args=[cls.post.pk])
        cls.REDIRECT_URL_LOGIN_COMMENT = f'{LOGIN}?next={cls.ADD_COMMENT_URL}'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_post_from_unauthorized_user(self):
        """Проверяем создание поста не авторизованным пользователем."""
        Post.objects.all().delete()
        form_data = {
            'text': 'Тестовый пост проверка',
            'group': self.group.id,
            'image': get_uploaded(),
        }
        response = self.guest.post(POST_CREATE_URL, data=form_data)
        self.assertRedirects(response, REDIRECT_LOGIN_URL)
        self.assertEqual(Post.objects.count(), 0)

    def test_edit_post_form(self):
        check_author_id = self.post.author_id
        form_data_edit = {
            'text': 'Тестовый текст изменен',
            'group': Group.objects.create(
                slug='test2-slug',
            ).id,
        }
        iteration_data = (
            (
                self.guest,
                self.post.group_id,
                self.post.text,
                '',
                'Неавторизованный клиент',
            ),
            (
                self.another,
                self.post.group_id,
                self.post.text,
                '',
                'Не автор',
            ),
            (
                self.author,
                form_data_edit['group'],
                form_data_edit['text'],
                f'{UPLOAD_PATH}Автор.gif',
                'Автор',
            ),
        )
        for client, group, text, img, description in iteration_data:
            with self.subTest(client_type=description):
                form_data_edit['image'] = get_uploaded(f'{description}.gif')
                client.post(
                    self.POST_EDIT_URL,
                    data=form_data_edit,
                )
                self.post.refresh_from_db()
                self.assertEqual(self.post.group_id, group)
                self.assertEqual(self.post.text, text)
                self.assertEqual(self.post.image.name, img)
                self.assertEqual(self.post.author_id, check_author_id)

    def test_create_post_from_authorized_user(self):
        """Провераем создание поста авторизованным пользователем."""
        Post.objects.all().delete()
        form_data_create = {
            'text': 'Тестовый текст для авторизованного',
            'group': self.group.id,
            'image': get_uploaded(),
        }
        response = self.author.post(POST_CREATE_URL, data=form_data_create)
        self.assertRedirects(response, PROFILE_URL)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.get()
        self.assertEqual(post.text, form_data_create['text'])
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group.id, form_data_create['group'])
        self.assertEqual(post.image, f'{UPLOAD_PATH}test_pic.gif')

    def test_create_comment(self):
        Comment.objects.all().delete()
        comment_data = {
            'text': 'Оставлю ка я тоже коментарий',
        }
        response = self.author.post(
            self.ADD_COMMENT_URL, data=comment_data, follow=True
        )
        self.assertRedirects(response, self.POST_DETAIL_URL)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.get()
        self.assertEqual(comment.text, comment_data['text'])
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)

    def test_create_comment_unauthorized_client(self):
        Comment.objects.all().delete()
        comment_data = {
            'text': 'Оставлю ка я тоже коментарий, но я не авторизован',
        }
        response = self.guest.post(
            self.ADD_COMMENT_URL, data=comment_data, follow=True
        )
        self.assertRedirects(response, self.REDIRECT_URL_LOGIN_COMMENT)
        self.assertEqual(Comment.objects.count(), 0)
