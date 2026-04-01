from django.test import TestCase
from django.contrib.auth import authenticate, get_user_model
from django.urls import reverse


User = get_user_model()


class EmailAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@etu.univ-amu.fr",
            password="StrongPassword123",
            first_name="Test",
            last_name="User",
        )

    def test_authenticate_with_email(self):
        user = authenticate(email="testuser@etu.univ-amu.fr", password="StrongPassword123")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "testuser@etu.univ-amu.fr")

    def test_authenticate_with_username_fallback(self):
        user = authenticate(username="testuser@etu.univ-amu.fr", password="StrongPassword123")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "testuser@etu.univ-amu.fr")

    def test_authenticate_with_wrong_password(self):
        user = authenticate(email="testuser@etu.univ-amu.fr", password="BadPwd")
        self.assertIsNone(user)

    def test_authenticate_with_unknown_email(self):
        user = authenticate(email="unknown@etu.univ-amu.fr", password="StrongPassword123")
        self.assertIsNone(user)

    def test_client_login_logout(self):
        login_success = self.client.login(email="testuser@etu.univ-amu.fr", password="StrongPassword123")
        self.assertTrue(login_success)

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        response_logout = self.client.get(reverse("logout"))
        self.assertRedirects(response_logout, reverse("signin"))

        response_after_logout = self.client.get(reverse("home"))
        self.assertEqual(response_after_logout.status_code, 200)
        self.assertFalse("testuser@etu.univ-amu.fr" in response_after_logout.content.decode())

    def test_signin_view_post_valid_credentials(self):
        response = self.client.post(
            reverse("signin"),
            {"email": "testuser@etu.univ-amu.fr", "password": "StrongPassword123"},
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertRedirects(response, reverse("home"))

    def test_signin_view_post_invalid_credentials(self):
        response = self.client.post(
            reverse("signin"),
            {"email": "testuser@etu.univ-amu.fr", "password": "wrong"},
            follow=True,
        )
        self.assertFalse(response.context["user"].is_authenticated)
        self.assertContains(response, "Email ou mot de passe incorrect.")
