from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'mistake-records', views.MistakeRecordViewSet, basename='mistake-record')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.get_profile, name='profile'),
    path('investment-types/', views.get_investment_types, name='investment-types'),
]
