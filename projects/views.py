from django.shortcuts import render
from .models import Project
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

# Create your views here.
def project_index(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'project_index.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {
        'project': project
    }
    return render(request, 'project_detail.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f"Contact from {form.cleaned_data['name']}",
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
            )
            return render(request, 'contact_success.html')
    else:
        form = ContactForm()
        
    return render(request, 'contact.html', {'form': form})