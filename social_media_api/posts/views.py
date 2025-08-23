from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, filters,status
from rest_framework.response import Response
from .serializers import  PostSerializer, CommentSerializer
from .models import Post, Comment


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission: only authors can edit/delete their posts or comments."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return obj.author == request.user

class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
# Create your views here.


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by("-created_at")

    def get(self, request):
        # Get the list of users the authenticated user follows
        following_users = request.user.following.all()

        # Fetch posts from those users
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        # Serialize posts
        feed = [
            {
                "id": post.id,
                "author": post.author.email,
                "content": post.content,
                "created_at": post.created_at,
            }
            for post in posts
        ]

        return Response(feed, status=status.HTTP_200_OK)
