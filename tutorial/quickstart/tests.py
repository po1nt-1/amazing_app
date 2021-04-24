from django.contrib.auth.models import User
from django.http import response
from django.test import TestCase
from tutorial.quickstart.models import Follow


class UsersTestCase(TestCase):
    def test_simple(self):
        self.assertEqual(1 + 1, 2)

    def test_unknown_url(self):
        response = self.client.get('/incorrect')
        self.assertEqual(response.status_code, 404)

    def test_emty_list_without_users(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })

    def test_list_users_with_users(self):
        User.objects.create(username='John')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    'id': 1,
                    'email': '',
                    'first_name': '',
                    'last_name': '',
                    'username': 'John'
                }
            ]
        })


class FollowTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='Kevin')
        self.user2 = User.objects.create(username='Tim')
        self.user3 = User.objects.create(username='Mo')
        Follow.objects.create(follower=self.user1, follows=self.user2)

    def test_data_exists(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Follow.objects.count(), 1)

    def test_new_follow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user3.username}/')
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(Follow.objects.get(
            follower=self.user1,
            follows=self.user3
        ))

    def test_unfollow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Follow.objects.count(), 0)

    def test_follow_yourself_failed(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(response.status_code, 400)
