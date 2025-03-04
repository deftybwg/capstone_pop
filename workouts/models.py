from django.db import models
from django.contrib.auth.models import User

class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)  # Monday, Tuesday, etc.
    column = models.IntegerField()  # Which column in the table
    value = models.TextField(blank=True, null=True)  # User's input

    def __str__(self):
        return f"{self.user.username} - {self.day} (Col {self.column}): {self.value}"
    
class WorkoutWeek(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return f"Week {self.number} - {self.user.username}"

class WorkoutEntry(models.Model):
    week = models.ForeignKey(WorkoutWeek, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    column = models.IntegerField()
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Week {self.week.number} - {self.day} (Col {self.column}): {self.value}"


