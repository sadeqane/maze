# Create your tests here.
from django.contrib.auth import get_user_model
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase


class Maze(APITestCase):
    maze = None

    def setUp(self) -> None:
        self.user = mommy.make(get_user_model(), username="test")

    def test_create_maze_success(self):
        self.client.force_login(self.user)
        url = "/maze/"
        payload = {
            "entrance": "A1",
            "grid_size": "8x8",
            "walls": """["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4", "B5", "E5", "B6", "D6", "E6", "G6", "H6", "B7", "D7", "G7", "B8"]"""
        }
        response = self.client.post(url, data=payload)
        self.maze = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_solve_maze_min_success(self):
        self.test_create_maze_success()
        self.client.force_login(self.user)
        url = f"/maze/{self.maze.get('id')}/solution?steps=min"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("path"), ['A1', 'B1', 'B2', 'B3', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'])
