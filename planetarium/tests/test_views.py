import tempfile
from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from planetarium.models import ShowTheme, AstronomyShow

User = get_user_model()


def get_temporary_image():
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file, format="JPEG")
    tmp_file.seek(0)
    return tmp_file


class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123"
        )
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )


class ShowThemeTests(AuthenticatedAPITestCase):
    def test_create_show_theme(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse("planetarium:showtheme-list"), {"name": "Stars"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_show_themes(self):
        ShowTheme.objects.create(name="Planets")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("planetarium:showtheme-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class AstronomyShowTests(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.admin)
        self.theme = ShowTheme.objects.create(name="Galaxy")

    def test_create_astronomy_show(self):
        data = {
            "title": "Big Bang",
            "description": "Story of the universe",
            "show_themes": [self.theme.id],
        }
        response = self.client.post(reverse("planetarium:astronomyshow-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_image(self):
        show = AstronomyShow.objects.create(title="Black Holes", description="Mystery", image=None)
        url = reverse("planetarium:astronomyshow-upload-image", args=[show.id])
        img = get_temporary_image()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, {"image": img}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        show.refresh_from_db()
        self.assertIsNotNone(show.image)
