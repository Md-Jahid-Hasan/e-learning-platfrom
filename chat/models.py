from django.contrib.auth import get_user_model
from django.db import models


class ChatData(models.Model):
    room_name = models.CharField(max_length=20)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=100)
    date = models.DateTimeField()
