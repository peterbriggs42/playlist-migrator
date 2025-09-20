import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Playlist Migrator API is running"
    assert data["version"] == "1.0.0"
    assert data["status"] == "healthy"

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Service is healthy"
    assert data["status"] == "healthy"

def test_get_users_empty():
    """Test getting users when none exist"""
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

def test_create_user():
    """Test creating a new user"""
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "status": "active"
    }
    
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["status"] == "active"
    assert "id" in data
    assert "created_at" in data

def test_get_user_by_id():
    """Test getting a user by ID"""
    # First create a user
    user_data = {
        "name": "Jane Doe",
        "email": "jane@example.com"
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # Then get the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"

def test_get_user_not_found():
    """Test getting a non-existent user"""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "User not found" in response.json()["error"]

def test_update_user():
    """Test updating a user"""
    # First create a user
    user_data = {
        "name": "Original Name",
        "email": "original@example.com"
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # Then update the user
    update_data = {
        "name": "Updated Name",
        "email": "updated@example.com"
    }
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["email"] == "updated@example.com"

def test_delete_user():
    """Test deleting a user"""
    # First create a user
    user_data = {
        "name": "To Delete",
        "email": "delete@example.com"
    }
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # Then delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify user is deleted
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404

def test_create_user_invalid_email():
    """Test creating a user with invalid email"""
    user_data = {
        "name": "Test User",
        "email": "invalid-email"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422  # Validation error

def test_create_user_missing_fields():
    """Test creating a user with missing required fields"""
    user_data = {
        "name": "Test User"
        # Missing email
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422  # Validation error
