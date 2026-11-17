import pytest
from rest_framework import status

from catalog.models import Category, Manufacturer, Part


@pytest.mark.django_db
def test_get_parts_empty_list(api_client):
    response = api_client.get('/parts/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_get_parts_list_anonymous(api_client, part):
    response = api_client.get('/parts/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == part.title


@pytest.mark.django_db
def test_get_parts_list_filters(api_client, part, category, manufacturer):
    other_category = Category.objects.create(name='GPU', description='Video cards')
    other_manufacturer = Manufacturer.objects.create(name='NVIDIA', country='USA')
    Part.objects.create(
        title='RTX 4070',
        category=other_category,
        manufacturer=other_manufacturer,
        price='25000.00',
        specs={'vram': 12},
    )

    response = api_client.get(
        f'/parts/?category={category.id}&manufacturer={manufacturer.id}&search=Ryzen'
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == part.id


@pytest.mark.django_db
def test_get_part_detail(api_client, part):
    response = api_client.get(f'/parts/{part.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == part.id
    assert response.data['title'] == part.title


@pytest.mark.django_db
def test_create_part_by_admin(admin_client, category, manufacturer):
    payload = {
        'title': 'Core i5-12400F',
        'category': category.id,
        'manufacturer': manufacturer.id,
        'price': '5200.00',
        'rating': '4.70',
        'specs': {'cores': 6},
        'description': 'Intel CPU',
    }
    response = admin_client.post('/parts/', data=payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Part.objects.count() == 1
    assert response.data['title'] == 'Core i5-12400F'


@pytest.mark.django_db
def test_update_part_put_by_admin(admin_client, part, category, manufacturer):
    payload = {
        'title': 'Ryzen 5 5600X',
        'category': category.id,
        'manufacturer': manufacturer.id,
        'price': '6000.00',
        'rating': '4.90',
        'specs': {'cores': 6, 'boost': '4.6GHz'},
        'description': 'Updated CPU',
    }
    response = admin_client.put(f'/parts/{part.id}/', data=payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Ryzen 5 5600X'
    updated_part = Part.objects.get(id=part.id)
    assert updated_part.title == 'Ryzen 5 5600X'


@pytest.mark.django_db
def test_partial_update_part_patch_by_admin(admin_client, part):
    response = admin_client.patch(
        f'/parts/{part.id}/',
        data={'price': '4999.00'},
        format='json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['price'] == '4999.00'
    updated_part = Part.objects.get(id=part.id)
    assert str(updated_part.price) == '4999.00'


@pytest.mark.django_db
def test_delete_part_by_admin(admin_client, part):
    response = admin_client.delete(f'/parts/{part.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Part.objects.count() == 0


@pytest.mark.django_db
def test_create_part_unauthenticated(api_client, category, manufacturer):
    payload = {
        'title': 'Unauthorized CPU',
        'category': category.id,
        'manufacturer': manufacturer.id,
        'price': '1000.00',
        'specs': {'cores': 4},
    }
    response = api_client.post('/parts/', data=payload, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_part_invalid_token(api_client, category, manufacturer):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
    payload = {
        'title': 'Invalid Token CPU',
        'category': category.id,
        'manufacturer': manufacturer.id,
        'price': '1000.00',
        'specs': {'cores': 4},
    }
    response = api_client.post('/parts/', data=payload, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_part_by_regular_user_forbidden(auth_client, category, manufacturer):
    payload = {
        'title': 'Forbidden CPU',
        'category': category.id,
        'manufacturer': manufacturer.id,
        'price': '1000.00',
        'specs': {'cores': 4},
    }
    response = auth_client.post('/parts/', data=payload, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_part_put_unauthenticated(api_client, part, category, manufacturer):
    payload = {
        'title': 'Unauthorized Put',
        'category': category.id,
        'manufacturer': manufacturer.id,
        'price': '1000.00',
        'specs': {'cores': 4},
    }
    response = api_client.put(f'/parts/{part.id}/', data=payload, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_part_put_by_regular_user_forbidden(auth_client, part, category, manufacturer):
    payload = {
        'title': 'Forbidden Put',
        'category': category.id,
        'manufacturer': manufacturer.id,
        'price': '1000.00',
        'specs': {'cores': 4},
    }
    response = auth_client.put(f'/parts/{part.id}/', data=payload, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_partial_update_part_patch_unauthenticated(api_client, part):
    response = api_client.patch(f'/parts/{part.id}/', data={'price': '1000.00'}, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_partial_update_part_patch_by_regular_user_forbidden(auth_client, part):
    response = auth_client.patch(f'/parts/{part.id}/', data={'price': '1000.00'}, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_part_unauthenticated(api_client, part):
    response = api_client.delete(f'/parts/{part.id}/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_part_by_regular_user_forbidden(auth_client, part):
    response = auth_client.delete(f'/parts/{part.id}/')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_part_invalid_data(admin_client, category, manufacturer):
    payload = {
        'title': 'Invalid CPU',
        'category': category.id,
        'manufacturer': manufacturer.id,
        'price': '-100.00',
        'specs': 'not-a-dict',
    }
    response = admin_client.post('/parts/', data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_nonexistent_part_not_found(api_client):
    response = api_client.get('/parts/99999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_nonexistent_part_not_found(admin_client):
    response = admin_client.delete('/parts/99999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_nonexistent_part_not_found(admin_client, category, manufacturer):
    payload = {
        'title': 'Missing CPU',
        'category': category.id,
        'manufacturer': manufacturer.id,
        'price': '1000.00',
        'specs': {'cores': 4},
    }
    response = admin_client.put('/parts/99999/', data=payload, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_part_invalid_data(admin_client, part, category, manufacturer):
    payload = {
        'title': 'Invalid CPU',
        'category': category.id,
        'manufacturer': manufacturer.id,
        'price': '-10.00',
        'specs': 'invalid',
    }
    response = admin_client.put(f'/parts/{part.id}/', data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_partial_update_nonexistent_part_not_found(admin_client):
    response = admin_client.patch('/parts/99999/', data={'price': '1000.00'}, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_partial_update_part_invalid_data(admin_client, part):
    response = admin_client.patch(
        f'/parts/{part.id}/',
        data={'price': '-5.00'},
        format='json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
