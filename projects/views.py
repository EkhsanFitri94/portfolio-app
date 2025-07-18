from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Project, Category, Comment, Tag, Like
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.db import models
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def project_index(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    tag_id = request.GET.get('tag')
    projects = Project.objects.filter(approved=True)
    if category_id:
        projects = projects.filter(category_id=category_id)
    if tag_id:
        projects = projects.filter(tags__id=tag_id)
    if query:
        projects = projects.filter(
            models.Q(title__icontains=query) |
            models.Q(technology__icontains=query)
        )
    categories = Category.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(projects, 6)  # Show 6 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "categories": categories,
        "tags": tags,
        "query": query,
        "page_obj": page_obj,
    }
    return render(request, "project_index.html", context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        name = request.POST.get("name")
        text = request.POST.get("text")
        if name and text:
            Comment.objects.create(project=project, name=name, text=text)
    comments = project.comments.order_by('-created_at')
    context = {
        'project': project,
        'comments': comments
    }
    return render(request, 'project_detail.html', context)

def contact_view(request):
    sent = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if name and email and message:
            send_mail(
                subject=f"Portfolio Contact from {name}",
                message=f"From: {name} <{email}>\n\n{message}",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
                recipient_list=["your@email.com"],  # Replace with your email
            )
            sent = True
    return render(request, "contact.html", {"sent": sent})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required
def like_project(request, pk):
    project = Project.objects.get(pk=pk)
    Like.objects.get_or_create(user=request.user, project=project)
    return HttpResponseRedirect(reverse('project_detail', args=[pk]))

@staff_member_required
def dashboard(request):
    from .models import Project, Comment, Like
    total_projects = Project.objects.count()
    total_comments = Comment.objects.count()
    total_likes = Like.objects.count()
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    context = {
        "total_projects": total_projects,
        "total_comments": total_comments,
        "total_likes": total_likes,
        "recent_comments": recent_comments,
    }
    return render(request, "dashboard.html", context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm  # You'll need to create this form

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_staff:
        return redirect('project_detail', pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, "edit_project.html", {"form": form, "project": project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_staff:
        return redirect('project_detail', pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect('project_index')
    return render(request, "delete_project.html", {"project": project})

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def profile(request):
    user = request.user
    comments = user.comment_set.all()  # If you linked comments to user
    liked_projects = Project.objects.filter(likes__user=user)
    context = {
        "user": user,
        "comments": comments,
        "liked_projects": liked_projects,
    }
    return render(request, "profile.html", context)

def about(request):
    skills = [
        {"name": "Python", "percent": 90},
        {"name": "Django", "percent": 85},
        {"name": "JavaScript", "percent": 80},
        {"name": "React", "percent": 75},
        {"name": "SQL", "percent": 70},
    ]
    return render(request, "about.html", {"skills": skills})