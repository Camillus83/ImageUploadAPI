from rest_framework.test import APITestCase
from accounts.models import CustomUser, Role
from django.contrib.auth import get_user_model
from PIL import Image as PILImage
from django.urls import reverse
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from io import BytesIO
import tempfile

# Create your tests here.
class APITestCase(APITestCase):
    User = get_user_model()

    def temporary_image(self):
        """
        Returns a new temporary image file
        """

        image = PILImage.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file, "jpeg")
        tmp_file.seek(
            0
        )  # important because after save(), the fp is already at the end of the file
        return tmp_file

    """"
       def test_upload_image(self):
        url = reverse('my_api_url')
        # Log in as the premium user
        self.client.login(username=self.premium_user.username, password='testpass123')
        # Open image file and convert it to bytes
        image_file = Image.open("path/to/image.jpg")
        image_bytes = io.BytesIO()
        image_file.save(image_bytes, format='JPEG')
        # Create InMemoryUploadedFile object with the image bytes
        image = InMemoryUploadedFile(
            image_bytes, None, 'image.jpg', 'image/jpeg', image_bytes.tell(), None
        )
        # Include the image in the data dictionary and send the POST request
        data = {'image': image}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    """

    def create_basic_user(self):
        return self.User.objects.create_user(
            username="basic_user",
            password="testpass123",
            role=Role.objects.get(name="Basic"),
        )

    def create_premium_user(self):
        return self.User.objects.create_user(
            username="premium_user",
            password="testpass123",
            role=Role.objects.get(name="Premium"),
        )

    def create_enterprise_user(self):
        return self.User.objects.create_user(
            username="enterprise_user",
            password="testpass123",
            role=Role.objects.get(name="Enterprise"),
        )

    def setUp(self):
        self.basic_user = self.create_basic_user()
        self.premium_user = self.create_premium_user()
        self.enterprise_user = self.create_enterprise_user()

    def test_post_image_basic_user(self):
        self.client.login(username=self.basic_user.username, password="testpass123")
        url = reverse("images")
        image = self.temporary_image()
        data = {"image": image}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("200px_thumbnail", response.data)
        self.assertNotIn("400px_thumbnail", response.data)
        thumbnail_url = response.data["200px_thumbnail"]["url"]
        thumbnail_response = self.client.get(thumbnail_url, format="multipart")

    def test_post_image_premium_user(self):
        self.client.login(username=self.premium_user.username, password="testpass123")

    def test_post_image_enterprise_user(self):
        self.client.login(
            username=self.enterprise_user.username, password="testpass123"
        )

    def test_get_image_basic_user(self):
        pass

    def test_get_image_premium_user(self):
        pass

    def test_get_image_enterprise_user(self):
        pass

    def test_post_not_image(self):
        pass
