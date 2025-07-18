from django.urls import path
from rest_framework import routers
from . import views
from .api_views import ProjectViewSet, CommentViewSet, LikeViewSet

router = routers.DefaultRouter()
router.register(r'api/projects', ProjectViewSet)
router.register(r'api/comments', CommentViewSet)
router.register(r'api/likes', LikeViewSet)

urlpatterns = [
    path('', views.project_index, name='project_index'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:pk>/like/', views.like_project, name='like_project'),
    path('about/', views.about, name='about'),
]
urlpatterns += router.urls
