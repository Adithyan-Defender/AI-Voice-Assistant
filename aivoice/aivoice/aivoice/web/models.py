from django.db import models
from django.conf import settings
from django.urls import reverse

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ Correct reference
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.user.email} at {self.timestamp}"

    def get_ai_chat_url(self):
        return reverse("web:ai_chat")


class UploadedImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    original_image = models.ImageField(upload_to='uploads/original/')
    processed_image = models.ImageField(upload_to='uploads/processed/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded by {self.user}"

    def get_background_remover_url(self):
        return reverse("web:background_remover")

    def get_image_generator_url(self):
        return reverse("web:image_generator")

    def get_home_url(self):
        return reverse("web:home")

    def get_about_url(self):
        return reverse("web:about_us")
