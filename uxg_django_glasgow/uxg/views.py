from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Community
from .forms import PostForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("post_list")  
    else:
        form = PostForm()
    
    return render(request, "uxg/createnewpost.html", {"form": form})

def index(request):
    posts = Post.objects.all().order_by("-created_at")  
    context_dict = {}
    context_dict['posts'] = posts
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

def signup(request):
    return render(request, "uxg/signup.html")

def login(request):
    return render(request, "uxg/login.html")

def profile(request):
    return render(request, "uxg/profile.html")