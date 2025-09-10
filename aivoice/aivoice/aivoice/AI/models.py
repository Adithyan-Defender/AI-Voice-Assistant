from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class JarvisResponse(models.Model):
    user_input = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_input[:50] 
    
    
    def get_home_url(self):
        return reverse("AI:ai_voice")