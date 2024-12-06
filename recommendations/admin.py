from django.contrib import admin
from .models import Recommendation, SavedRecommendation

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'impact', 'difficulty', 'carbon_saved')

@admin.register(SavedRecommendation)
class SavedRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommendation', 'saved_at']

