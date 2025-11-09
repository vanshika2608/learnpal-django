from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class LearningGoal(models.Model):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    STATUS_CHOICES = [
        (NOT_STARTED, "Not started"),
        (IN_PROGRESS, "In progress"),
        (DONE, "Completed"),
    ]

    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_STARTED)
    progress = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    tags = models.CharField(max_length=120, blank=True, help_text="Comma separated, e.g. python, algorithms")
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.title


class Resource(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    topic = models.CharField(max_length=120, help_text="e.g. python, dsa, ml, dbms")
    goal = models.ForeignKey(LearningGoal, null=True, blank=True, on_delete=models.SET_NULL, related_name="resources")
    is_bookmarked = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
