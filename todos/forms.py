from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'category', 'priority', 'due_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'What needs to be done?...',
                'class': 'task-input',
                'autocomplete': 'off',
                'required': 'required',
            }),
            'category': forms.Select(attrs={
                'class': 'task-select',
            }),
            'priority': forms.Select(attrs={
                'class': 'task-select',
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'task-date-input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Add details or notes (optional)...',
                'class': 'task-textarea',
                'rows': 2,
            }),
        }
        labels = {
            'title': 'Task Title',
            'category': 'Category',
            'priority': 'Priority Level',
            'due_date': 'Due Date',
            'description': 'Description',
        }


class UpdateTodo(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'category', 'priority', 'due_date', 'description', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Update task title...',
                'class': 'task-input',
                'autocomplete': 'off',
                'required': 'required',
            }),
            'category': forms.Select(attrs={
                'class': 'task-select',
            }),
            'priority': forms.Select(attrs={
                'class': 'task-select',
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'task-date-input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Update details or notes...',
                'class': 'task-textarea',
                'rows': 3,
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'task-checkbox',
            }),
        }
        labels = {
            'title': 'Task Title',
            'category': 'Category',
            'priority': 'Priority Level',
            'due_date': 'Due Date',
            'description': 'Description',
            'is_completed': 'Mark as Completed',
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address (optional)',
            'class': 'auth-input',
            'autocomplete': 'email',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choose a username',
            'class': 'auth-input',
            'autocomplete': 'username',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create password',
            'class': 'auth-input',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password',
            'class': 'auth-input',
            'autocomplete': 'new-password',
        })


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'auth-input',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'auth-input',
            'autocomplete': 'current-password',
        })
    )