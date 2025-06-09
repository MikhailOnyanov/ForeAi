import logging

from fastapi.testclient import TestClient

from ..main import app


LOGGER = logging.getLogger(__name__)


client = TestClient(app)

def test_read_users():
    response = client.get('/customer_service/users')
    LOGGER.info(f'test_read_users response: {response.json()}')
    assert response.status_code == 200
    # assert response.json() == {"name": "Foo", "description": "A test item"}

# def test_read_item_not_found():
#     response = client.get("/items/bar")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Item not found"}
#
# def test_create_item():
#     new_item = {"name": "Bar", "description": "Another test item"}
#     response = client.post("/items/bar", json=new_item)
#     assert response.status_code == 200
#     assert response.json() == new_item
#
# def test_create_item_already_exists():
#     new_item = {"name": "Foo", "description": "Duplicate item"}
#     response = client.post("/items/foo", json=new_item)
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Item already exists"}