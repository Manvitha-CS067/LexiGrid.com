from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Crossword(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    grid = models.JSONField()
    across_clues = models.JSONField()
    down_clues = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['-created_at']
class UserCrosswordProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    crossword = models.ForeignKey(Crossword, on_delete=models.SET_NULL, null=True)
    progress_grid = models.JSONField(default=list)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s progress on crossword {self.crossword_id}"

