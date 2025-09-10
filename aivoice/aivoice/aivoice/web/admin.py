from django.contrib import admin
from .models import ChatMessage,UploadedImage

admin.site.register(ChatMessage),

admin.site.register(UploadedImage)
