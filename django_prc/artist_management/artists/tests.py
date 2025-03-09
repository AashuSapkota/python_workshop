from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Artists

class ArtistAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist = Artists.objects.create(
            name="Test Artist",
            dob="1990-01-01T00:00:00Z",
            gender="m",
            address="Test Address",
            first_release_year="2010",
            no_of_albums_released=5
        )
        self.valid_artist_data = {
            "name": "New Artist",
            "dob": "1985-05-10T00:00:00Z",
            "gender": "f",
            "address": "New Address",
            "first_release_year": "2005",
            "no_of_albums_released": 3
        }

    def test_register_artist(self):
        url = reverse('artists:register_artist')
        response = self.client.post(url, self.valid_artist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Status'], 'Success')

    def test_list_artists(self):
        url = reverse('artists:list_artist')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_artist(self):
        url = reverse('artists:update_artist', kwargs={'artist_id': self.artist.id})
        updated_data = {
            "name": "Updated Artist Name",
            "dob": "1990-01-01T00:00:00Z",
            "gender": "x",
            "address": "Updated Address",
            "first_release_year": "2010",
            "no_of_albums_released": 6
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Status'], 'Success')


    def test_delete_artist(self):
        url = reverse('artists:delete_artist', kwargs={'artist_id': self.artist.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Status'], 'Success')
        self.assertFalse(Artists.objects.filter(id=self.artist.id).exists())
