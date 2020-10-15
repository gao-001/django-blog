from rest_framework import generics,viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser
from .models import Post
from .serializer import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    permission_classes = [IsAdminUser]