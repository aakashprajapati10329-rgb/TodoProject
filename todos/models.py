from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):

    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    CATEGORY_CHOICES = [
        ('COLLEGE', '🎓 College Work'),
        ('HOMEWORK', '📚 Homework'),
        ('WORK', '💼 Work / Office'),
        ('PERSONAL', '🏠 Personal'),
        ('FITNESS', '🏃 Fitness & Health'),
        ('SHOPPING', '🛒 Shopping / Errand'),
        ('OTHER', '📌 General / Other'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='todos'
    )

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='COLLEGE'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    due_date = models.DateField(
        blank=True,
        null=True
    )

    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_completed', '-created_at']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title} ({self.priority})"