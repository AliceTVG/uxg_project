
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Community,Profile
from .forms import PostForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserUpdateForm, ProfileUpdateForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth import logout
from .forms import BioForm



import json

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("index")  
    else:
        form = PostForm()
    
    return render(request, "uxg/createnewpost.html", {"form": form})

def index(request):
    posts = Post.objects.all().order_by("-created_at")  
    context_dict = {
        'posts': posts,
        'MEDIA_URL': settings.MEDIA_URL  
    }
    return render(request, "uxg/index.html", context=context_dict)


def community_page(request):
    return render(request, 'uxg/communities.html')

def community_detail_page(request, community_id):
    """Render the frontend page for a specific community."""
    community = get_object_or_404(Community, id=community_id)
    return render(request, 'uxg/community_detail.html', {'community': community})

@csrf_exempt
def community_list(request):
    """Handles fetching all communities and creating new ones."""
    if request.method == "GET":
        # Return all communities
        communities = Community.objects.all().values('id', 'name', 'description', 'created_at')
        return JsonResponse(list(communities), safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            description = data.get("description")

            if not name or not description:
                return JsonResponse({"error": "Name and description are required."}, status=400)

            community, created = Community.objects.get_or_create(name=name, defaults={"description": description})

            if not created:
                return JsonResponse({"error": "Community already exists."}, status=400)

            return JsonResponse({"message": "Community created successfully!", "id": community.id}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)


def community_detail(request, community_id):
    """Return details of a single community by ID."""
    community = get_object_or_404(Community, id=community_id)
    data = {
        'id': community.id,
        'name': community.name,
        'description': community.description,
        'created_at': community.created_at
    }
    return JsonResponse(data)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('uxg:profile')

  

    else:
        form = AuthenticationForm()

    return render(request, 'uxg/login.html', {'form': form})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() 

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.bio = profile_form.cleaned_data['bio']
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            profile.save()

            registered = True
            messages.success(request, "You have successfully signed up!")
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileUpdateForm()

    return render(request, 'uxg/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'uxg/profile.html', context)
def logout_view(request):
    logout(request)
    return redirect('uxg:index')

def edit_bio(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = BioForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('uxg:profile')
    else:
        form = BioForm(instance=profile)

    return render(request, 'uxg/edit_bio.html', {'form': form})