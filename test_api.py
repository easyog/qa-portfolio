"""API-тесты к публичному учебному API (JSONPlaceholder).

Покрывают позитивные и негативные кейсы: статус-коды, схему и типы ответа,
коллекции, создание ресурса, параметризованные чтения.
"""
import requests
import pytest

BASE = "https://jsonplaceholder.typicode.com"
TIMEOUT = 20


def test_get_post_returns_200():
    r = requests.get(f"{BASE}/posts/1", timeout=TIMEOUT)
    assert r.status_code == 200


def test_get_post_json_structure():
    r = requests.get(f"{BASE}/posts/1", timeout=TIMEOUT)
    data = r.json()

    # обязательные поля присутствуют
    for field in ("userId", "id", "title", "body"):
        assert field in data, f"нет поля '{field}'"

    # типы соответствуют контракту
    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert data["id"] == 1


def test_get_list_is_not_empty():
    r = requests.get(f"{BASE}/posts", timeout=TIMEOUT)
    assert r.status_code == 200
    posts = r.json()
    assert isinstance(posts, list)
    assert len(posts) > 0


def test_missing_resource_returns_404():
    # несуществующий ресурс должен возвращать 404, а не чужие данные
    r = requests.get(f"{BASE}/posts/999999", timeout=TIMEOUT)
    assert r.status_code == 404


def test_create_post_returns_201():
    payload = {"title": "QA test", "body": "hello", "userId": 1}
    r = requests.post(f"{BASE}/posts", json=payload, timeout=TIMEOUT)

    assert r.status_code == 201
    created = r.json()
    assert created["title"] == "QA test"
    assert "id" in created


@pytest.mark.parametrize("post_id", [1, 2, 3, 50, 100])
def test_many_posts_accessible(post_id):
    r = requests.get(f"{BASE}/posts/{post_id}", timeout=TIMEOUT)
    assert r.status_code == 200
    assert r.json()["id"] == post_id
