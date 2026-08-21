from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'priority', 'due_date', 'is_completed', 'created_at')
    list_filter = ('category', 'priority', 'is_completed', 'created_at')
    search_fields = ('title', 'description', 'category', 'user__username')
    ordering = ('-created_at',)
