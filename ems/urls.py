from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ems import views

router = DefaultRouter()
router.register(r'company', views.CompanyViewSet)
router.register(r'department', views.DepartmentViewSet)
router.register(r'employee', views.EmployeeViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
