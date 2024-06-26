from builtins import str
import pytest
from httpx import AsyncClient
from datetime import timedelta
from unittest.mock import AsyncMock, patch
from app.main import app
from app.models.user_model import User, UserRole
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token, create_access_token  # Import your FastAPI app

# Example of a test function using the async_client fixture
@pytest.mark.asyncio
async def test_create_user_access_denied(async_client, user_token, email_service):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Define user data for the test
    user_data = {
        "nickname": generate_nickname(),
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    # Send a POST request to create a user
    response = await async_client.post("/users/", json=user_data, headers=headers)
    # Asserts
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_user_duplicate_email_admin(async_client, db_session, admin_token):
    user_data_1 = {
            "nickname": "user1",
            "first_name": "User",
            "last_name": "One",
            "email": "user1@example.com",
            "hashed_password": hash_password("AnotherPassword$5678"),
            "role": UserRole.AUTHENTICATED,
            "email_verified": True,
            "is_locked": False,
        }
    first_user = User(**user_data_1)
    db_session.add(first_user)
    await db_session.commit()
    user_data_2 = {
            "nickname": "user2",
            "email": "user1@example.com",
            "password": "AnotherPassword$5678",
        }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/users/", json=user_data_2, headers=headers)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_create_user_duplicate_nickname_admin(async_client, db_session, admin_token):
    user_data_1 = {
            "nickname": "user1",
            "first_name": "User",
            "last_name": "One",
            "email": "user1@example.com",
            "hashed_password": hash_password("AnotherPassword$5678"),
            "role": UserRole.AUTHENTICATED,
            "email_verified": True,
            "is_locked": False,
        }
    first_user = User(**user_data_1)
    db_session.add(first_user)
    await db_session.commit()
    user_data_2 = {
            "nickname": "user1",
            "email": "user2@example.com",
            "password": "AnotherPassword$5678",
        }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/users/", json=user_data_2, headers=headers)
    assert response.status_code == 400

# You can similarly refactor other test functions to use the async_client fixture
@pytest.mark.asyncio
async def test_retrieve_user_access_denied(async_client, verified_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get(f"/users/{verified_user.id}", headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_retrieve_user_access_allowed(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)

@pytest.mark.asyncio
async def test_update_user_email_access_denied(async_client, verified_user, user_token):
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(f"/users/{verified_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client, admin_user, admin_token):
    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]

@pytest.mark.asyncio
async def test_update_user_duplicate_email(async_client, db_session, user, admin_token):
    user_data = {
            "nickname": "user1",
            "first_name": "User",
            "last_name": "One",
            "email": "user1@example.com",
            "hashed_password": hash_password("AnotherPassword$5678"),
            "role": UserRole.AUTHENTICATED,
            "email_verified": True,
            "is_locked": False,
        }
    first_user = User(**user_data)
    db_session.add(first_user)
    user
    await db_session.commit()
    updated_data = {"email": "user1@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{user.id}", json=updated_data, headers=headers)
    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_update_user_duplicate_nickname(async_client, db_session, user, admin_token):
    user_data = {
            "nickname": "user2",
            "first_name": "User",
            "last_name": "Two",
            "email": "user2@example.com",
            "hashed_password": hash_password("AnotherPassword$5678"),
            "role": UserRole.AUTHENTICATED,
            "email_verified": True,
            "is_locked": False,
        }
    first_user = User(**user_data)
    db_session.add(first_user)
    user
    await db_session.commit()
    updated_data = {"nickname": "user2"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{user.id}", json=updated_data, headers=headers)
    assert response.status_code == 400
    assert "Nickname already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_delete_user(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{admin_user.id}", headers=headers)
    assert delete_response.status_code == 204
    # Verify the user is deleted
    fetch_response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert fetch_response.status_code == 404

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "AnotherPassword123!",
        "role": UserRole.ADMIN.name
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert "Email or Nickname already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_create_user_duplicate_nickname(async_client, verified_user):
    user_data = {
        "email": "AnotherEmail123@example.com",
        "password": "AnotherPassword123!",
        "nickname": verified_user.nickname,
        "role": UserRole.ADMIN.name
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert "Email or Nickname already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    user_data = {
        "email": "notanemail",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

import pytest
from app.services.jwt_service import decode_token
from urllib.parse import urlencode

@pytest.mark.asyncio
async def test_login_success(async_client, verified_user):
    # Attempt to login with the test user
    form_data = {
        "username": verified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    # Check for successful login response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Use the decode_token method from jwt_service to decode the JWT
    decoded_token = decode_token(data["access_token"])
    assert decoded_token is not None, "Failed to decode token"
    assert decoded_token["role"] == "AUTHENTICATED", "The user role should be AUTHENTICATED"

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    form_data = {
        "username": "nonexistentuser@here.edu",
        "password": "DoesNotMatter123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_incorrect_password(async_client, verified_user):
    form_data = {
        "username": verified_user.email,
        "password": "IncorrectPassword123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_unverified_user(async_client, unverified_user):
    form_data = {
        "username": unverified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_locked_user(async_client, locked_user):
    form_data = {
        "username": locked_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400
    assert "Account locked due to too many failed login attempts." in response.json().get("detail", "")
@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, admin_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"  # Valid UUID format
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert delete_response.status_code == 404

@pytest.mark.asyncio
async def test_update_user_github(async_client, admin_user, admin_token):
    updated_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == updated_data["github_profile_url"]

@pytest.mark.asyncio
async def test_update_user_linkedin(async_client, admin_user, admin_token):
    updated_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["linkedin_profile_url"] == updated_data["linkedin_profile_url"]

@pytest.mark.asyncio
async def test_list_users_as_admin(async_client, admin_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert 'items' in response.json()

@pytest.mark.asyncio
async def test_list_users_as_manager(async_client, manager_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_users_invalid_skip_integer(async_client, admin_token):
    response = await async_client.get(
        "/users/",
        params={"skip": -1},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Skip integer cannot be less than 0"

@pytest.mark.asyncio
async def test_list_users_invalid_limit_integer(async_client, admin_token):
    response = await async_client.get(
        "/users/",
        params={"limit": 0},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Limit integer cannot be less than 1"

@pytest.mark.asyncio
async def test_list_users_unauthorized(async_client, user_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden, as expected for regular user

@pytest.mark.asyncio
async def test_update_user_profile_access_denied_with_fake_token(async_client):
    headers = {"Authorization": f"Bearer fake_token"}
    updated_user_data = {
        "nickname": "NicknameTest123",
        "email": "test@example.com",
        "first_name": "TestUpdate",
        "last_name": "TestUpdate",
        "bio": "TestBio",
        "profile_picture_url": "https://www.example.com/test.jpg",
        "linkedin_profile_url": "https://www.linkedin.com/test",
        "github_profile_url": "https://www.github.com/test"
    }
    response = await async_client.put("/update-profile/", json=updated_user_data, headers=headers)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_user_profile(async_client, verified_user_and_token):
    user, token = verified_user_and_token
    headers = {"Authorization": f"Bearer {token}"}
    updated_user_data = {
        "first_name": "TestUpdate",
        "last_name": "TestUpdate",
        "bio": "TestBio",
        "profile_picture_url": "https://www.example.com/test.jpg",
        "linkedin_profile_url": "https://www.linkedin.com/test",
        "github_profile_url": "https://www.github.com/test"
    }
    response = await async_client.put("/update-profile/", json=updated_user_data, headers=headers)  
    assert response.status_code == 200
    assert response.json()["first_name"] == updated_user_data["first_name"]

@pytest.mark.asyncio
async def test_update_user_profile_duplicate_nickname(async_client, db_session, verified_user_and_token):
    first_user, token = verified_user_and_token
    user_data_2 = {
            "nickname": "user2",
            "first_name": "User",
            "last_name": "Two",
            "email": "user2@example.com",
            "hashed_password": hash_password("AnotherPassword$5678"),
            "role": UserRole.AUTHENTICATED,
            "email_verified": True,
            "is_locked": False,
        }
    second_user = User(**user_data_2)
    db_session.add(second_user)
    await db_session.commit()

    headers = {"Authorization": f"Bearer {token}"}
    updated_user_data = {
        "nickname": "user2",
    }
    response = await async_client.put("/update-profile/", json=updated_user_data, headers=headers)  
    assert response.status_code == 400
    assert response.json()["detail"] == "Nickname already exists"

@pytest.mark.asyncio
async def test_update_user_profile_duplicate_email(async_client, db_session, verified_user_and_token):
    first_user, token = verified_user_and_token
    user_data_2 = {
            "nickname": "user2",
            "first_name": "User",
            "last_name": "Two",
            "email": "user2@example.com",
            "hashed_password": hash_password("AnotherPassword$5678"),
            "role": UserRole.AUTHENTICATED,
            "email_verified": True,
            "is_locked": False,
        }
    second_user = User(**user_data_2)
    db_session.add(second_user)
    await db_session.commit()

    headers = {"Authorization": f"Bearer {token}"}
    updated_user_data = {
        "email": "user2@example.com",
    }
    response = await async_client.put("/update-profile/", json=updated_user_data, headers=headers)  
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

@pytest.mark.asyncio
async def test_update_user_professional_status_access_denied_with_fake_token(async_client):
    fake_token = "fake_token"
    update_data = {"is_professional": True}
    response = await async_client.put("/users/user_id/set-professional/true", headers={"Authorization": f"Bearer {fake_token}"}, json=update_data)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_user_professional_status_access_denied_with_user_token(async_client, user_token):
    token = user_token
    update_data = {"is_professional": True}
    response = await async_client.put("/users/user_id/set-professional/true", headers={"Authorization": f"Bearer {token}"}, json=update_data)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_professional_status_as_admin(async_client, admin_token, verified_user):
    update_data_true = {"is_professional": True}
    update_data_false = {"is_professional": False}
    headers = {"Authorization": f"Bearer {admin_token}"}
    professional_user = verified_user
    
    # Mock the email service
    with patch('app.services.email_service.EmailService.send_professional_status_email') as mock_send_email:
        mock_send_email.return_value = None  # Mock the email sending
        
        response = await async_client.put(f"/users/{professional_user.id}/set-professional/true", headers=headers, json=update_data_true)
        assert response.status_code == 200
        assert response.json()["is_professional"] == True

        response = await async_client.put(f"/users/{professional_user.id}/set-professional/false", headers=headers, json=update_data_false)
        assert response.status_code == 200
        assert response.json()["is_professional"] == False
