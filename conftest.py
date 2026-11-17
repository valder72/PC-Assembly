import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from catalog.models import Category, Manufacturer, Part


@pytest.fixture(scope="function")
def api_client():
    yield APIClient()


@pytest.fixture(scope="function")
def regular_user():
    yield User.objects.create_user(
        username='regular_user',
        email='user@example.com',
        password='password123',
        is_staff=False,
    )


@pytest.fixture(scope="function")
def admin_user():
    yield User.objects.create_user(
        username='admin_user',
        email='admin@example.com',
        password='password123',
        is_staff=True,
    )


def _authenticate_client(api_client, user, password):
    login_url = reverse('token_obtain_pair')
    tokens = api_client.post(
        login_url,
        {'username': user.username, 'password': password},
        format='json',
    ).data
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    return api_client


@pytest.fixture(scope="function")
def auth_client(api_client, regular_user):
    yield _authenticate_client(api_client, regular_user, 'password123')


@pytest.fixture(scope="function")
def admin_client(api_client, admin_user):
    yield _authenticate_client(api_client, admin_user, 'password123')


@pytest.fixture(scope="function")
def category():
    yield Category.objects.create(
        name='CPU',
        description='Processors',
    )


@pytest.fixture(scope="function")
def manufacturer():
    yield Manufacturer.objects.create(
        name='AMD',
        country='USA',
    )


@pytest.fixture(scope="function")
def part(category, manufacturer):
    yield Part.objects.create(
        title='Ryzen 5 5600',
        category=category,
        manufacturer=manufacturer,
        price='5500.00',
        rating='4.80',
        specs={'cores': 6, 'threads': 12},
        description='6-core CPU',
    )
