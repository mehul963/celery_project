from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_http_methods
from .forms import UserCreationForm,LeadForm
from .models import CustomUser,Lead
from .tasks import count

def dashboard(request):
    x=count.apply_async()
    print(x)
    if request.user.is_authenticated:
        return redirect('/leads')
    return render(request,"index.html")

@require_http_methods(['GET','POST'])
def _login(request):
    if request.user.is_authenticated:
        return redirect('/leads')
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        user=authenticate(request,email=email,password=password)
        if not user:
            print(user)
            return redirect('/')
        login(request,user=user)
        return redirect('/leads')
    return render(request,'index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('/leads')
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("User created")
    return render(request,'index.html')
        


def _logout(request):
    logout(request)
    return redirect("/")


def leads(request):
    
    leads = Lead.objects.filter(handlers=request.user).order_by('-id')
    if request.user.is_superuser:
        leads = Lead.objects.all().order_by('-id')
    users=CustomUser.objects.filter(is_superuser=False)
    context = {'leads': leads,'users':users}
    return render(request, 'leads.html', context)

from .tasks import assign_lead
def create_lead(request):
    if request.method == 'POST':
        # form = LeadForm(request.POST)
        # if form.is_valid():
        #     form.save()
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        lead=Lead(name=name,phone=phone)
        lead.save()
        return redirect('/leads')  # Redirect to the lead list page after successful creation
    else:
        form = LeadForm()
    return render(request, 'create_lead.html', {'form': form})

def create_staff_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff=True
            user.save()
            return redirect('/leads')  # Redirect to the staff user list page after successful creation
    else:
        form = UserCreationForm()
    return render(request, 'add_user.html', {'form': form})