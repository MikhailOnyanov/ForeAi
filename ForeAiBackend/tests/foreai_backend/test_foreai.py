import asyncio

import httpx
import pytest
import pytest_asyncio


BASE_URL = 'http://localhost'
test_collection = 'fore_collection'

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
    response = await async_client.post('/customer_service/users/', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'phone_number': '+1234567890',
        'is_active': True
    })
    assert response.status_code == 200
    return response.json()


@pytest_asyncio.fixture
async def test_collection(async_client):
    name = 'fore_collection'
    response = await async_client.post('/data/create_collection/', json={'collection_name': name})
    assert response.status_code == 200
    return name


@pytest.mark.asyncio
async def test_list_collections(async_client):
    response = await async_client.get('/data/list_collections')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_process_documentation(async_client, test_collection='fore_collection'):
    params = {'collection_name': test_collection, 'save_locally': False}
    response = await async_client.get('/docs/process_documentation', params=params)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_vector(async_client, test_collection='fore_collection'):
    params = {'collection_name': test_collection, 'message': 'What is ForeAi?'}
    response = await async_client.get('/docs/get_vector', params=params)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_generate_response(async_client):
    response = await async_client.get('/message/generate_response', params={'message': 'Hello!'})
    assert response.status_code == 200
