# Sustainable_platform/urls.py

# from django.contrib import admin
# from django.urls import path, include
# from recommendations import views as recommendations_views 

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('register/', recommendations_views.register, name='register'),
#     path('home/', recommendations_views.home, name='home'),
#     path('recommendations/', include('recommendations.urls')),
# ]

# In Sustainable_platform/urls.py
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView , LogoutView
from recommendations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='recommendations/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('saved/', views.saved, name='saved'),
    path('tracker/', views.tracker, name='tracker'),
    path('mark_as_completed/', views.mark_as_completed, name='mark_as_completed'),
    path('settings/', views.settings, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('recommendations/', views.recommendations, name='recommendations'), 
    path('save-recommendation/', views.save_recommendation, name='save_recommendation'),
    path('remove_saved_recommendation/<int:id>/', views.remove_saved_recommendation, name='remove_saved_recommendation'),

]


