# recommendations/urls.py

from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # path('recommendations/', views.recommendations, name='recommendations'), 
    # path('recommendations/', views.recommend_based_on_preference, name='recommend_based_on_preference'),
    path('save-recommendation/', views.save_recommendation, name='save_recommendation'),
    path('remove_saved_recommendation/<int:id>/', views.remove_saved_recommendation, name='remove_saved_recommendation'),
    path('saved/',views.saved, name='saved'),
    path('tracker/', views.tracker, name='tracker'),
    path('mark_as_completed/', views.mark_as_completed, name='mark_as_completed'),
    path('settings/', views.settings, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),


]

