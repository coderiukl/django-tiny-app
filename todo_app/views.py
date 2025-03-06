from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    form = TaskForm()  # Tạo form mới để không bị mất ô điền task
    tasks = []
    if request.user.is_authenticated:  # Chỉ hiển thị task nếu user đăng nhập
        tasks = Task.objects.filter(user=request.user, is_deleted=False, is_archieved=False)
    
    paginator = Paginator(tasks, 4)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'home.html', {'tasks': page_obj, 'form': form})
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
    
    paginator = Paginator(task_archieved, 4)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'tasks_archieved':page_obj}
    return render(request, 'archieved.html', context=context)

@login_required(login_url='/signin/')
def delete_task(request):
    task_deleted = Task.objects.filter(user=request.user, is_archieved=False, is_deleted=True)
    
    paginator = Paginator(task_deleted, 4)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'tasks_deleted':page_obj}
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
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Login successful! Welcome back 🎉")
                    return redirect('home')  # Chuyển hướng về trang chủ
                else:
                    messages.error(request, "Your account has been blocked.")
                    return redirect('signin')
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

# Quản lý user - admin chỉ có thể xem danh sách người dùng và thực hiện các thao tác
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, "manage_users.html", {'users': users})

# Khóa hoặc mở khóa user
@user_passes_test(is_admin)
def toggle_block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Không cho phép admin khóa chính tài khoản của mình
    if user == request.user:
        messages.error(request, "You cannot block your own account.")
        return redirect('manage_users')
    
    # Khóa hoặc mở khóa tài khoản user
    user.is_active = not user.is_active  # Khóa user bằng cách thay đổi trạng thái is_active
    user.save()
    status = "blocked" if not user.is_active else "unblocked"
    messages.success(request, f"User {user.username} has been {status}.")
    return redirect('manage_users')

# Reset mật khẩu cho user
@user_passes_test(is_admin)
def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Nếu user đang bị khóa, thông báo và không cho phép reset mật khẩu
    if not user.is_active:
        messages.error(request, "User account is blocked. Cannot reset password.")
        return redirect('manage_users')
    
    if request.method == "POST":
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Cập nhật session sau khi đổi mật khẩu
            messages.success(request, f"Password for {user.username} has been reset.")
            return redirect('manage_users')
    else:
        form = PasswordChangeForm(user)

    return render(request, 'reset_password.html', {'form': form, 'user': user})