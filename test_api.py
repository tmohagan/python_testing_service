import pytest
import requests
from config import API_URL
from config import API_URL, TEST_CREDENTIALS

def login():
    response = requests.post(f"{API_URL}/login", json=TEST_CREDENTIALS)
    assert response.status_code == 200
    return response.cookies.get('token'), response.cookies

def test_create_and_delete_post():
    # Login
    token, cookies = login()
    headers = {'Cookie': f'token={token}'}

    # Create a post
    test_data = {
        "title": "Test Post for Deletion",
        "summary": "This is a test post that will be deleted",
        "content": "This is the content of the test post that will be deleted"
    }
    create_response = requests.post(f"{API_URL}/post", json=test_data, headers=headers, cookies=cookies)
    assert create_response.status_code == 200
    created_post = create_response.json()
    assert "title" in created_post
    assert created_post["title"] == test_data["title"]
    assert "_id" in created_post

    # Get the ID of the created post
    post_id = created_post["_id"]

    # Delete the post
    delete_response = requests.delete(f"{API_URL}/post/{post_id}", headers=headers, cookies=cookies)
    assert delete_response.status_code == 200
    delete_result = delete_response.json()
    assert delete_result["success"] == True

    # Verify the post is deleted by trying to fetch it
    get_response = requests.get(f"{API_URL}/post/{post_id}")
    assert get_response.status_code == 404  # Assuming your API returns 404 for non-existent posts

def test_get_posts():
    response = requests.get(f"{API_URL}/post")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert isinstance(data["posts"], list)

def test_get_single_post():
    # First, get all posts to find a valid ID
    response = requests.get(f"{API_URL}/post")
    posts = response.json()["posts"]
    
    if len(posts) > 0:
        post_id = posts[0]["_id"]
        response = requests.get(f"{API_URL}/post/{post_id}")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "content" in data
    else:
        pytest.skip("No posts available to test")

def test_get_projects():
    response = requests.get(f"{API_URL}/project")
    assert response.status_code == 200
    data = response.json()
    assert "projects" in data
    assert isinstance(data["projects"], list)

def test_get_single_project():
    # First, get all projects to find a valid ID
    response = requests.get(f"{API_URL}/project")
    projects = response.json()["projects"]
    
    if len(projects) > 0:
        project_id = projects[0]["_id"]
        response = requests.get(f"{API_URL}/project/{project_id}")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "content" in data
    else:
        pytest.skip("No projects available to test")

def test_create_and_delete_project():
    # Login
    token, cookies = login()
    headers = {'Cookie': f'token={token}'}

    # Create a project
    test_data = {
        "title": "Test Project for Deletion",
        "summary": "This is a test project that will be deleted",
        "content": "This is the content of the test project that will be deleted",
        "demo": "testdemo"
    }
    create_response = requests.post(f"{API_URL}/project", json=test_data, headers=headers, cookies=cookies)
    assert create_response.status_code == 200
    created_project = create_response.json()
    assert "title" in created_project
    assert created_project["title"] == test_data["title"]
    assert "_id" in created_project

    # Get the ID of the created project
    project_id = created_project["_id"]

    # Verify the project was created
    get_response = requests.get(f"{API_URL}/project/{project_id}")
    assert get_response.status_code == 200
    assert get_response.json()["_id"] == project_id

    # Delete the project
    delete_response = requests.delete(f"{API_URL}/project/{project_id}", headers=headers, cookies=cookies)
    assert delete_response.status_code == 200
    delete_result = delete_response.json()
    assert delete_result["success"] == True

    # Verify the project is deleted by trying to fetch it
    get_response = requests.get(f"{API_URL}/project/{project_id}")
    assert get_response.status_code == 404

    # Additional check: try to delete the project again
    delete_response = requests.delete(f"{API_URL}/project/{project_id}", headers=headers, cookies=cookies)
    assert delete_response.status_code == 404

def test_update_post():
    # Login
    token, cookies = login()
    headers = {'Cookie': f'token={token}'}

    # Create a post
    test_data = {
        "title": "Test Post for Update",
        "summary": "This is a test post that will be updated",
        "content": "This is the content of the test post that will be updated"
    }
    create_response = requests.post(f"{API_URL}/post", json=test_data, headers=headers, cookies=cookies)
    assert create_response.status_code == 200
    created_post = create_response.json()
    post_id = created_post["_id"]

    # Update the post
    update_data = {
        "title": "Updated Test Post",
        "summary": "This is an updated test post",
        "content": "This is the updated content of the test post",
        "id": post_id
    }
    update_response = requests.put(f"{API_URL}/post", json=update_data, headers=headers, cookies=cookies)
    assert update_response.status_code == 200
    updated_post = update_response.json()
    assert updated_post["title"] == update_data["title"]

    # Clean up by deleting the post
    delete_response = requests.delete(f"{API_URL}/post/{post_id}", headers=headers, cookies=cookies)
    assert delete_response.status_code == 200

def test_update_project():
    # Login
    token, cookies = login()
    headers = {'Cookie': f'token={token}'}

    # Create a project
    test_data = {
        "title": "Test Project for Update",
        "summary": "This is a test project that will be updated",
        "content": "This is the content of the test project that will be updated",
        "demo": "testdemo"
    }
    create_response = requests.post(f"{API_URL}/project", json=test_data, headers=headers, cookies=cookies)
    assert create_response.status_code == 200
    created_project = create_response.json()
    project_id = created_project["_id"]

    # Update the project
    update_data = {
        "title": "Updated Test Project",
        "summary": "This is an updated test project",
        "content": "This is the updated content of the test project",
        "demo": "updateddemo",
        "id": project_id
    }
    update_response = requests.put(f"{API_URL}/project", json=update_data, headers=headers, cookies=cookies)
    assert update_response.status_code == 200
    updated_project = update_response.json()
    
    # Check if all fields were updated correctly
    assert updated_project["title"] == update_data["title"]
    assert updated_project["summary"] == update_data["summary"]
    assert updated_project["content"] == update_data["content"]
    assert updated_project["demo"] == update_data["demo"]

    # Verify the update by fetching the project again
    get_response = requests.get(f"{API_URL}/project/{project_id}")
    assert get_response.status_code == 200
    fetched_project = get_response.json()
    assert fetched_project["title"] == update_data["title"]

    # Clean up by deleting the project
    delete_response = requests.delete(f"{API_URL}/project/{project_id}", headers=headers, cookies=cookies)
    assert delete_response.status_code == 200

def test_invalid_login():
    credentials = {
        "username": "invaliduser",
        "password": "invalidpassword"
    }
    response = requests.post(f"{API_URL}/login", json=credentials)
    assert response.status_code == 400
    assert "error" in response.json()
    assert response.json()["error"] == "Wrong credentials"

def test_valid_login():
    response = requests.post(f"{API_URL}/login", json=TEST_CREDENTIALS)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "username" in response.json()
    assert "token" in response.cookies

def test_pagination():
    # Test pagination for posts
    response = requests.get(f"{API_URL}/post?page=1&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert len(data["posts"]) <= 5

    # Test pagination for projects
    response = requests.get(f"{API_URL}/project?page=1&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "projects" in data
    assert len(data["projects"]) <= 5