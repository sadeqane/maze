from django.core.validators import validate_comma_separated_integer_list
from django.db import models


# Create your models here.


class Maze(models.Model):
    entrance = models.CharField(max_length=2)
    grid_size = models.CharField(max_length=100)
    walls = models.CharField(max_length=1000, validators=[validate_comma_separated_integer_list])
    owner = models.ForeignKey("account.User", on_delete=models.CASCADE)