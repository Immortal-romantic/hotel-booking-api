"""
URL configuration for hotel_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import JsonResponse

def api_info(request):
    """Информация о доступных API эндпоинтах"""
    return JsonResponse({
        "message": "🏨 Hotel Booking API",
        "version": "1.0",
        "endpoints": {
            "rooms": {
                "create": "POST /rooms/create",
                "list": "GET /rooms/list", 
                "delete": "POST /rooms/delete"
            },
            "bookings": {
                "create": "POST /bookings/create",
                "list": "GET /bookings/list",
                "delete": "POST /bookings/delete"
            }
        },
        "example": "curl -X POST -d 'description=Люкс' -d 'price_per_night=5000' http://localhost:9000/rooms/create"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_info, name='api_info'),  # Главная страница с информацией об API
    path('', include('rooms.urls')),      # Подключаем URLs из приложения rooms
    path('', include('bookings.urls')),   # Подключаем URLs из приложения bookings
]


