import os
import django

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uxg_django_glasgow.settings")
django.setup()

from django.contrib.auth.models import User
from uxg.models import Community, Post


def populate():
    # Create users
    user1, _ = User.objects.get_or_create(username="testuser1", email="user1@example.com")
    user2, _ = User.objects.get_or_create(username="testuser2", email="user2@example.com")
    
    # Create communities
    maths, _ = Community.objects.get_or_create(name="Mathematics", description="Discuss maths courses!")
    games, _ = Community.objects.get_or_create(name="Gaming", description="For all gamers!")

    # Create posts
    posts = [
        {"user": user1, "community": maths, "content": "WHY DID I TAKE MATHS1 :("},
        {"user": user2, "community": games, "content": "Just beat Elden Ring for the 10th time!"},
    ]

    for post_data in posts:
        Post.objects.create(**post_data)

    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
