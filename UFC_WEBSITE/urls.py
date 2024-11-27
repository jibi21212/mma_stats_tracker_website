"""
URL configuration for UFC_WEBSITE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("myapp.urls"))
    # Forwards myapp/ to include("myapp.urls")
]

# Allows us to route to different django applications
# myapp/home
# Path["", include("myapp.urls")]
# So myapp will be handled here, and then go into the other url file which then handles the home part
# This allows us to have applications that have simular names, such as things like the word home, many applications can have a home
# By having the extra prefix of myapp it allows us to distinguish that we are talking about home of myapp without having to have distinct names for everything