from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    preferences = models.JSONField(default=dict)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recommendation(models.Model):
    carbon_saved = models.DecimalField(max_digits=10, decimal_places=2)
    difficulty = models.IntegerField()
    impact = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Adjust as needed
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    

    def __str__(self):
        return self.title


class SavedRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)  # Progress feature (e.g., 0-100%)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.recommendation.title} ({self.progress}%)"
    
class CompletedRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.recommendation.title} (Completed at {self.completed_at})"