from django.test import TestCase
from .models import Project

class ProjectModelTest(TestCase):
    def test_create_project(self):
        project = Project.objects.create(
            title="Test Project",
            description="Test Description",
            technology="Django",
            image="test.jpg"
        )
        self.assertEqual(project.title, "Test Project")
