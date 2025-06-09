import asyncio
import uuid

import httpx
import pytest
import pytest_asyncio


BASE_URL = 'http://localhost'


@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        yield client


@pytest_asyncio.fixture
async def created_user(async_client):
    unique_email = f'test_{uuid.uuid4()}@example.com'
    response = await async_client.post('/customer_service/users/', json={
        'name': 'Test User',
        'email': unique_email,
        'phone_number': '+1234567890',
        'is_active': True
    })
    assert response.status_code == 200
    user = response.json()
    yield user
    try:
        await async_client.delete(f"/customer_service/users/{user['uuid']}")
    except Exception:
        pass
    
    # ------------------ Users ------------------

@pytest.mark.asyncio
async def test_create_user(async_client):
    unique_email = f'test_{uuid.uuid4()}@example.com'
    response = await async_client.post('/customer_service/users/', json={
        'name': 'Alice',
        'email': unique_email,
        'phone_number': '+123456789',
        'is_active': True
    })
    assert response.status_code == 200
    assert response.json()['email'] == unique_email


@pytest.mark.asyncio
async def test_read_users(async_client):
    response = await async_client.get('/customer_service/users/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_user(async_client, created_user):
    user_id = created_user['uuid']
    response = await async_client.patch(f'/customer_service/users/{user_id}',
                                        json={'name': 'Alice Updated'})
    assert response.status_code == 200
    assert response.json()['name'] == 'Alice Updated'


@pytest.mark.asyncio
async def test_delete_user(async_client, created_user):
    user_id = created_user['uuid']
    response = await async_client.delete(f'/customer_service/users/{user_id}')
    assert response.status_code == 200
