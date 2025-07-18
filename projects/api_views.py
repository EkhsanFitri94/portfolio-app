from rest_framework import viewsets
from .models import Project, Comment, Like
from .serializers import ProjectSerializer, CommentSerializer, LikeSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(approved=True)
    serializer_class = ProjectSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer