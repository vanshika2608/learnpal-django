from django.test import TestCase
from .models import LearningGoal, Resource

class LearningGoalModelTest(TestCase):
    def setUp(self):
        self.goal = LearningGoal.objects.create(
            title="Learn Django",
            description="Understand forms and models",
            progress=20,
            priority=3  # 3 = High
        )

    def test_goal_creation(self):
        self.assertEqual(self.goal.title, "Learn Django")
        self.assertEqual(self.goal.progress, 20)
        self.assertEqual(str(self.goal), "Learn Django")


class ResourceModelTest(TestCase):
    def setUp(self):
        self.resource = Resource.objects.create(
            title="Django Docs",
            url="https://docs.djangoproject.com/",
            topic="Django"
        )

    def test_resource_creation(self):
        self.assertEqual(self.resource.topic, "Django")
        self.assertTrue(self.resource.url.startswith("https"))
