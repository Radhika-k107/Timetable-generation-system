# timetable_generator/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('timetable.urls')),  # Include the timetable app's URLs
]