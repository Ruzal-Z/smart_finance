from django.test import TestCase
from django.urls import reverse
from posts.urls import app_name

POST_ID = 1
SLUG = 'slug'
NAME = 'username'
ROUTES = [
    ('index', [], '/'),
    ('group_list', [SLUG], f'/group/{SLUG}/'),
    ('profile', [NAME], f'/profile/{NAME}/'),
    ('post_detail', [POST_ID], f'/posts/{POST_ID}/'),
    ('post_create', [], '/create/'),
    ('post_edit', [POST_ID], f'/posts/{POST_ID}/edit/'),
    ('add_comment', [POST_ID], f'/posts/{POST_ID}/comment/'),
    ('follow_index', [], '/follow/'),
    ('profile_follow', [NAME], f'/profile/{NAME}/follow/'),
    ('profile_unfollow', [NAME], f'/profile/{NAME}/unfollow/'),
]


class TestRoutes(TestCase):
    def test_routes(self):
        for name, args, expected_url in ROUTES:
            with self.subTest(expected_url=expected_url):
                self.assertEqual(
                    reverse(f'{app_name}:{name}', args=args), expected_url
                )
