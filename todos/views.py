from django.shortcuts import render, redirect,get_object_or_404
from .models import Todo
from .forms import TodoForm,UpdateTodo
# Create your views here.
def home(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TodoForm()
        
    tasks = Todo.objects.all().order_by('id')
    return render(request, 'home.html', {'tasks': tasks, 'form': form})
def update(request, id):
    task = get_object_or_404(Todo, id=id)

    if request.method == 'POST':
        form = UpdateTodo(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = UpdateTodo(instance=task)

    return render(request, 'update.html', {'form': form})





def delete(request, id):
    task = get_object_or_404(Todo, id=id)

    if request.method == 'POST':
        task.delete()
        return redirect('home')

    return render(request, 'delete_confirmation.html', {'task': task})                              