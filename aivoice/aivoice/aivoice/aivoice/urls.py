from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("web.urls",namespace="home")),
    path("ai/",include("AI.urls",namespace="AI")),
    path("accounts/",include("accounts.urls",namespace="accounts")),
]