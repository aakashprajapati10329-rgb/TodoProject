from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'What needs to be done?...',
                'class': 'task-input',
                'autocomplete': 'off',
            })
        }
        labels = {
            'title': 'Task Title'
        }


class UpdateTodo(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Update task title...',
                'class': 'task-input',
                'autocomplete': 'off',
            })
        }
        labels = {
            'title': 'Task Title'
        }