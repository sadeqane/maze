from django.urls import path
from rest_framework.routers import DefaultRouter

from account.views import UserViewSet
from maze.views import MazeView, SolveMazeView

router = DefaultRouter()
router.register('', MazeView, basename='maze')

urlpatterns = router.urls

urlpatterns += [
    path('<int:maze_id>/solution', SolveMazeView.as_view({'get': 'retrieve'}), name="maze-solution"),
]
