from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.http import HttpResponse

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