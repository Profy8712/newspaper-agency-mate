from typing import Self
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from newspaper.models import Newspaper, Topic

User = get_user_model()


class SearchTestCase(TestCase):
    def setUp(self: Self) -> None:
        self.client = Client()

        # Create test topics
        self.topic1 = Topic.objects.create(name='Politics')
        self.topic2 = Topic.objects.create(name='Technology')

        # Create test redactors
        self.redactor1 = User.objects.create_user(
            username='john_doe',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            years_of_experience=5,
            password='testpass123'
        )
        self.redactor2 = User.objects.create_user(
            username='jane_smith',
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            years_of_experience=3,
            password='testpass123'
        )

        # Create test newspapers
        self.newspaper1 = Newspaper.objects.create(
            title='Global Summit on Climate Change',
            content='World leaders gathered to discuss climate policies...',
            published_date=timezone.now().date(),
            topic=self.topic1
        )
        self.newspaper1.publishers.add(self.redactor1)

        self.newspaper2 = Newspaper.objects.create(
            title='New AI Breakthrough Announced',
            content='Scientists developed a new AI model that...',
            published_date=timezone.now().date(),
            topic=self.topic2
        )
        self.newspaper2.publishers.add(self.redactor2)

        # Login a test user
        self.client.login(username='john_doe', password='testpass123')


class TopicSearchTests(SearchTestCase):
    def test_topic_search_by_name(self: Self) -> None:
        response = self.client.get(
            reverse('newspaper:topic-list'),
            {'name': 'Politics'}
        )
        self.assertContains(response, self.topic1.name)
        self.assertNotContains(response, self.topic2.name)

    def test_topic_partial_search(self: Self) -> None:
        response = self.client.get(
            reverse('newspaper:topic-list'),
            {'name': 'Tech'}
        )
        self.assertContains(response, self.topic2.name)
        self.assertNotContains(response, self.topic1.name)


class NewspaperSearchTests(SearchTestCase):
    def test_newspaper_search_by_title(self: Self) -> None:
        response = self.client.get(
            reverse('newspaper:newspaper-list'),
            {'title': 'Global Summit'}
        )
        self.assertContains(response, self.newspaper1.title)
        self.assertNotContains(response, self.newspaper2.title)

    def test_newspaper_search_by_content(self: Self) -> None:
        response = self.client.get(
            reverse('newspaper:newspaper-list'),
            {'title': 'AI model'}
        )
        self.assertContains(response, self.newspaper2.title)
        self.assertNotContains(response, self.newspaper1.title)


class RedactorSearchTests(SearchTestCase):
    def test_redactor_search_by_username(self: Self) -> None:
        response = self.client.get(
            reverse('newspaper:redactor-list'),
            {'username': 'jane'}
        )
        # More robust check — test actual search results, not full HTML
        self.assertIn(self.redactor2, response.context["object_list"])
        self.assertNotIn(self.redactor1, response.context["object_list"])

    def test_redactor_search_by_experience(self: Self) -> None:
        response = self.client.get(
            reverse('newspaper:redactor-list'),
            {'years': '5'}
        )
        self.assertIn(self.redactor1, response.context["object_list"])
        self.assertNotIn(self.redactor2, response.context["object_list"])


class PaginationWithSearchTests(SearchTestCase):
    def test_pagination_maintains_search(self: Self) -> None:
        # Create enough newspapers to trigger pagination
        for i in range(15):
            Newspaper.objects.create(
                title=f'Test Newspaper {i}',
                content=f'Content for newspaper {i}',
                published_date=timezone.now().date(),
                topic=self.topic1
            )

        response = self.client.get(
            reverse('newspaper:newspaper-list'),
            {'title': 'Test', 'page': '2'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'title=Test')
        self.assertContains(response, 'page=2')


class NewspaperFilterByTopicTests(SearchTestCase):
    def test_filter_newspapers_by_topic(self: Self) -> None:
        response = self.client.get(
            reverse('newspaper:newspaper-list'),
            {'topic': self.topic1.id}
        )
        self.assertContains(response, self.newspaper1.title)
        self.assertNotContains(response, self.newspaper2.title)


class RedactorDetailTests(SearchTestCase):
    def test_redactor_detail_shows_newspapers(self: Self) -> None:
        response = self.client.get(
            reverse(
                'newspaper:redactor-detail',
                kwargs={'pk': self.redactor1.pk}
            )
        )
        self.assertContains(response, self.newspaper1.title)
        self.assertNotContains(response, self.newspaper2.title)
