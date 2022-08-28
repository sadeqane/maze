from django.shortcuts import render, get_object_or_404
import numpy as np

# Create your views here.
from rest_framework import mixins
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from maze.filters import IsOwnerFilterBackend
from maze.helpers import MinPath, MaxPath, create_matrix, walls_to_matrix
from maze.models import Maze
from maze.serializers import MazeSerializer, SolveMazeSerializer

import ast


class MazeView(mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    queryset = Maze.objects.all()
    serializer_class = MazeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [IsOwnerFilterBackend]


class SolveMazeView(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = SolveMazeSerializer
    permission_classes = [IsAuthenticated]

    def validate(self, maze_id, steps):
        try:
            maze = get_object_or_404(Maze, pk=maze_id)
        except:
            raise NotFound
        if maze.owner != self.request.user:
            raise PermissionDenied("You are not the owner of this Maze")
        if steps not in ["min", "max"]:
            raise ValidationError("Steps query param should be one of `min` or `max`")

    def retrieve(self, request, *args, **kwargs):
        """
            Return a list of all users.
            """
        try:
            maze_id = kwargs.get("maze_id")
            steps = request.query_params.get("steps")
        except Exception as e:
            raise ValidationError(e)

        self.validate(maze_id, steps)
        path = []
        maze = Maze.objects.get(pk=maze_id)
        m = int(tuple(maze.grid_size)[0])
        n = int(tuple(maze.grid_size)[2])
        walls = ast.literal_eval(maze.walls)
        matrix = create_matrix(m, n)
        walls_matrix = create_matrix(m, n)
        walls_to_matrix(walls, walls_matrix)
        if steps == "min":
            # solve min
            obj = MinPath(
                m=m,
                n=n,
                walls_matrix=walls_matrix,
                entrance=maze.entrance,
            )
            path, exited_point = obj.solve()
        elif steps == "max":
            # first solve min to detect exited point
            obj = MinPath(
                m=m,
                n=n,
                walls_matrix=walls_matrix,
                entrance=maze.entrance,
            )
            path, exited_point = obj.solve()

            # second solve max
            reverse_walls = np.where((walls_matrix == 0) | (walls_matrix == 1), walls_matrix ^ 1, walls_matrix)
            obj = MaxPath(m=m, n=n, entrance=maze.entrance, destination=exited_point, walls_matrix=reverse_walls)
            path, max = obj.solve()

        return Response(SolveMazeSerializer({"path": path}).data)
