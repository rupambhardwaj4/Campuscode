from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Problem, Contest, ForumPost

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('index')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name 
        user.role = 'Student'
        user.streak = 1
        user.global_rank = 9999
        user.college_rank = 500
        user.xp = 100
        user.save()

        login(request, user)
        return redirect('dashboard')
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == 'Admin':
                return redirect('admin_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('index')
    return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

@login_required
def problems(request):
    problems = Problem.objects.all()
    return render(request, 'problems.html', {'problems': problems})

@login_required
def solve_problem(request, id):
    problem = get_object_or_404(Problem, id=id)
    return render(request, 'problem_page.html', {'problem': problem})

@login_required
def contests(request):
    contests = Contest.objects.order_by('start_time')
    return render(request, 'contest.html', {'contests': contests})

@login_required
def contest_overview(request, id):
    contest = get_object_or_404(Contest, id=id)
    return render(request, 'contest_overview.html', {'contest': contest})

@login_required
def forum(request):
    posts = ForumPost.objects.order_by('-date_posted')
    return render(request, 'forum.html', {'posts': posts})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def stats(request):
    return render(request, 'report.html')

@login_required
def admin_dashboard(request):
    if request.user.role != 'Admin': return redirect('dashboard')
    stats = {
        'users': User.objects.filter(role='Student').count(),
        'problems': Problem.objects.count(),
        'contests': Contest.objects.count()
    }
    return render(request, 'admin_dashboard.html', {'stats': stats})

@login_required
def add_problem(request):
    if request.method == 'POST':
        Problem.objects.create(
            title=request.POST.get('title'),
            difficulty=request.POST.get('difficulty'),
            points=request.POST.get('points'),
            tags=request.POST.get('tags'),
            statement=request.POST.get('statement'),
            input_fmt=request.POST.get('input_fmt'),
            output_fmt=request.POST.get('output_fmt'),
            constraints=request.POST.get('constraints'),
            sample_input=request.POST.get('sample_input'),
            sample_output=request.POST.get('sample_output')
        )
        messages.success(request, 'Problem Added')
    return redirect('admin_dashboard')

@login_required
def add_contest(request):
    if request.method == 'POST':
        Contest.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            rules=request.POST.get('rules'),
            prizes=request.POST.get('prizes'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            status='Upcoming'
        )
        messages.success(request, 'Contest Created')
    return redirect('admin_dashboard')