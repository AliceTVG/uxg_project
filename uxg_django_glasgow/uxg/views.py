from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
from .models import Community
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


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