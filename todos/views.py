import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Todo
from .forms import TodoForm, UpdateTodo, UserRegisterForm, UserLoginForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['just_logged_in'] = True
            messages.success(request, f"Welcome to TaskMaster, {user.username}! Your account has been created.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['just_logged_in'] = True
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, "Task added successfully!")
            return redirect('home')
    else:
        form = TodoForm()

    # User's tasks
    user_tasks = Todo.objects.filter(user=request.user)

    # Check for login popup notification (< 24 hours / overdue / due today)
    today = timezone.localdate()
    tomorrow = today + datetime.timedelta(days=1)
    
    show_due_modal = False
    due_soon_tasks = []
    if request.session.pop('just_logged_in', False):
        due_soon_tasks = user_tasks.filter(
            is_completed=False,
            due_date__isnull=False,
            due_date__lte=tomorrow
        ).order_by('due_date', 'priority')
        if due_soon_tasks.exists():
            show_due_modal = True

    # Stats calculation
    total_count = user_tasks.count()
    completed_count = user_tasks.filter(is_completed=True).count()
    pending_count = user_tasks.filter(is_completed=False).count()
    high_priority_count = user_tasks.filter(is_completed=False, priority='HIGH').count()

    stats = {
        'total': total_count,
        'completed': completed_count,
        'pending': pending_count,
        'high_priority': high_priority_count,
    }

    # Filtering, Sorting & Search
    status_filter = request.GET.get('status', 'all')
    priority_filter = request.GET.get('priority', 'all')
    category_filter = request.GET.get('category', 'all')
    sort_by = request.GET.get('sort', 'created_desc')
    search_query = request.GET.get('q', '').strip()

    filtered_tasks = user_tasks

    # Status Filter
    if status_filter == 'pending':
        filtered_tasks = filtered_tasks.filter(is_completed=False)
    elif status_filter == 'completed':
        filtered_tasks = filtered_tasks.filter(is_completed=True)

    # Priority Filter
    if priority_filter in ['HIGH', 'MEDIUM', 'LOW']:
        filtered_tasks = filtered_tasks.filter(priority=priority_filter)

    # Category Filter
    valid_categories = [c[0] for c in Todo.CATEGORY_CHOICES]
    if category_filter in valid_categories:
        filtered_tasks = filtered_tasks.filter(category=category_filter)

    # Search Query
    if search_query:
        filtered_tasks = filtered_tasks.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    # Sorting
    from django.db.models import F, Case, When, Value, IntegerField
    if sort_by == 'due_date':
        filtered_tasks = filtered_tasks.order_by('is_completed', F('due_date').asc(nulls_last=True), '-created_at')
    elif sort_by == 'priority':
        priority_order = Case(
            When(priority='HIGH', then=Value(1)),
            When(priority='MEDIUM', then=Value(2)),
            When(priority='LOW', then=Value(3)),
            default=Value(4),
            output_field=IntegerField()
        )
        filtered_tasks = filtered_tasks.order_by('is_completed', priority_order, '-created_at')
    elif sort_by == 'title':
        filtered_tasks = filtered_tasks.order_by('is_completed', 'title')
    elif sort_by == 'created_asc':
        filtered_tasks = filtered_tasks.order_by('is_completed', 'created_at')
    else:
        filtered_tasks = filtered_tasks.order_by('is_completed', '-created_at')

    context = {
        'tasks': filtered_tasks,
        'form': form,
        'stats': stats,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'category_filter': category_filter,
        'category_choices': Todo.CATEGORY_CHOICES,
        'sort_by': sort_by,
        'search_query': search_query,
        'show_due_modal': show_due_modal,
        'due_soon_tasks': due_soon_tasks,
        'today': today,
        'tomorrow': tomorrow,
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def toggle_complete(request, id):
    task = get_object_or_404(Todo, id=id, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    status_msg = "completed" if task.is_completed else "marked as pending"
    messages.info(request, f"Task '{task.title}' {status_msg}.")
    return redirect('home')


@login_required(login_url='login')
def update(request, id):
    task = get_object_or_404(Todo, id=id, user=request.user)

    if request.method == 'POST':
        form = UpdateTodo(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated successfully!")
            return redirect('home')
    else:
        form = UpdateTodo(instance=task)

    return render(request, 'update.html', {'form': form, 'task': task})


@login_required(login_url='login')
def delete(request, id):
    task = get_object_or_404(Todo, id=id, user=request.user)

    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.warning(request, f"Task '{task_title}' deleted.")
        return redirect('home')

    return render(request, 'delete_confirmation.html', {'task': task})