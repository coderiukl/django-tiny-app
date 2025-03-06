from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    form = TaskForm()  # Tạo form mới để không bị mất ô điền task
    tasks = []
    if request.user.is_authenticated:  # Chỉ hiển thị task nếu user đăng nhập
        tasks = Task.objects.filter(user=request.user, is_deleted=False, is_archieved=False)

    return render(request, 'home.html', {'tasks': tasks, 'form': form})
@login_required  # Chỉ cho phép user đã đăng nhập thêm task
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user  # Gán task cho user đang đăng nhập
            obj.save()
    return redirect('home')

@login_required(login_url='/signin/')
def archieve_task(request):
    task_archieved = Task.objects.filter(user=request.user, is_archieved=True, is_deleted=False)
    context = {'tasks_archieved':task_archieved}
    return render(request, 'archieved.html', context=context)

@login_required(login_url='/signin/')
def delete_task(request):
    task_deleted = Task.objects.filter(user=request.user, is_archieved=False, is_deleted=True)
    context = {'tasks_deleted':task_deleted}
    return render(request, 'deleted.html', context=context)

def update_task(request, pk):
    obj = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
    else:
        action = request.GET.get('action')
        if action == "is_completed":
            obj.is_completed = not obj.is_completed
        elif action == 'is_archieved':
            obj.is_archieved = not obj.is_archieved
            obj.is_deleted = False
        elif action == 'is_deleted':
            obj.is_archieved = False
            obj.is_deleted = not obj.is_deleted
        else:
            return redirect('home')
        obj.save()
    return redirect(request.META.get('HTTP_REFERER'))

def empty_recycle_bin(request):
    obj = Task.objects.filter(is_deleted=True)
    obj.delete()
    return redirect('deleted')

# Login and Logout, Registration

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful! Welcome back 🎉")
                return redirect('home')  # Chuyển hướng về trang chủ
            else:
                messages.error(request, "Invalid username or password!")  # Hiển thị lỗi
                return render(request, "signin.html", {"loginform": form})  # Render lại trang login với lỗi
    else:
        form = LoginForm()

    return render(request, "signin.html", {"loginform": form})


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registraion successful! Welcome 🎉")
            return redirect('home')
        else:
            messages.error(request, "Registraion failed. Please check the form.")
    else:
        form = RegistrationForm()
    context = {'signupform':form}
    return render(request, 'signup.html', context=context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully. 🎉")
    return redirect('home')

# Phần của admin
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin, login_url='/')
def admin_user_list(request):
    users = User.objects.all()
    return render(request, 'admin_user_list.html', {'users':users})
