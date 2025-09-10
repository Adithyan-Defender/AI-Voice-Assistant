from django.urls import path

from web import views


app_name="web"

urlpatterns=[
    path("",views.Home,name="home"),
    path("ai_chat",views.AIChat,name="ai_chat"),
    path("background_remover",views.bgRemover,name="background_remover"),
    path("image_generator",views.imgGeneration,name="image_generator"),
    path("about_us",views.about_us,name="about_us"),
 
]