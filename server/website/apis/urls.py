from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, CategoryViewSet, CourseViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
