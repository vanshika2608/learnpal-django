from django.test import TestCase, Client
from django.urls import reverse
from .models import LearningGoal, Resource

class GoalsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.goals_home_url = reverse('goals_home')
        self.edit_goal_url_name = 'edit_goal'
        self.delete_goal_url_name = 'delete_goal'

    def test_goals_home_get(self):
        response = self.client.get(self.goals_home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_add_goal_post_valid(self):
        data = {
            'title': 'Test Goal',
            'description': 'Test Description',
            'status': 'NOT_STARTED',
            'progress': 0,
            'due_date': '',
            'priority': '3',
            'tags': 'test,goal'
        }
        response = self.client.post(self.goals_home_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(LearningGoal.objects.filter(title='Test Goal').exists())

    def test_add_goal_post_invalid(self):
        data = {
            'title': '',  # Title required
            'description': 'Test Description',
            'status': 'NOT_STARTED',
            'progress': 0,
            'due_date': '',
            'priority': '3',
            'tags': 'test,goal'
        }
        response = self.client.post(self.goals_home_url, data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        form = response.context['form']
        self.assertFormError(form, 'title', 'This field is required.')

    def test_edit_goal(self):
        goal = LearningGoal.objects.create(title='Edit Goal', progress=10, priority=3)
        url = reverse(self.edit_goal_url_name, args=[goal.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {
            'title': 'Edited Goal',
            'description': 'Edited Description',
            'status': 'IN_PROGRESS',
            'progress': 50,
            'due_date': '',
            'priority': '2',
            'tags': 'edited'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        goal.refresh_from_db()
        self.assertEqual(goal.title, 'Edited Goal')
        self.assertEqual(goal.progress, 50)

    def test_delete_goal(self):
        goal = LearningGoal.objects.create(title='Delete Goal', progress=10, priority=3)
        url = reverse(self.delete_goal_url_name, args=[goal.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(LearningGoal.objects.filter(id=goal.id).exists())

class ResourcesViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.resources_url = reverse('resources')
        self.add_resource_url = reverse('add_resource')

    def test_resources_list_get(self):
        response = self.client.get(self.resources_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/resources.html')

    def test_add_resource_post_valid(self):
        data = {
            'title': 'Test Resource',
            'url': 'https://example.com',
            'topic': 'Test',
            'goal': '',
            'is_bookmarked': False
        }
        response = self.client.post(self.add_resource_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Resource.objects.filter(title='Test Resource').exists())

    def test_add_resource_post_invalid(self):
        data = {
            'title': '',
            'url': 'invalid-url',
            'topic': '',
            'goal': '',
            'is_bookmarked': False
        }
        response = self.client.post(self.add_resource_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect even on error
        self.assertFalse(Resource.objects.filter(title='').exists())
