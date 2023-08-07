import pytest
from run import app


keys_should_be_posts = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count",
                        "pk"}


def test_get_posts_json():
    """Тестируем возвращение всех постов"""
    response = app.test_client().get("/api/posts/")
    posts = response.json
    assert type(posts) == list, "Возвращается не список"
    assert set(posts[0].keys()) == keys_should_be_posts, "Неправильные ключи"


def test_get_single_post_json():
    """Тестируем возвращение поста по id"""
    response = app.test_client().get("/api/posts/1/")
    post = response.json
    assert type(post) == dict, "Возвращается не словарь"
    assert set(post.keys()) == keys_should_be_posts, "Неправильные ключи"
