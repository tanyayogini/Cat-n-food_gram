from utils import *
import pytest

keys_should_be_posts = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count",
                        "pk"}

keys_should_be_comments = {"post_id", "commenter_name", "comment", "pk"}


def test_get_posts_all():
    posts = get_posts_all()
    assert type(posts) == list, "Возвращается не список"
    assert len(posts) > 0, "Возвращается пустой список"
    assert set(posts[0].keys()) == keys_should_be_posts, "Неверный список ключей"


def test_get_posts_by_user():
    posts = get_posts_by_user("leo")
    assert type(posts) == list, "Возвращается не список"
    assert posts[0]["poster_name"].lower() == "leo", "Возвращаются посты неправильного автора"
    assert len(posts) == 2, "Возвращается неправильное количество постов"
    assert set(posts[0].keys()) == keys_should_be_posts, "Неверный список ключей"


def test_get_posts_by_user_value_error():
    with pytest.raises(ValueError):
        get_posts_by_user("test_name")


def test_get_comments_by_post_id():
    comments = get_comments_by_post_id(1)
    assert type(comments) == list, "Возвращается не список"
    assert comments[0]["post_id"] == 1, "Возвращает посты с неправильным id"
    assert len(comments) == 4, "Возвращается неправильное количество постов"
    assert set(comments[0].keys()) == keys_should_be_comments, "Возвращаются неправильные ключи"


def test_get_comments_by_post_id_value_error():
    with pytest.raises(ValueError):
        get_comments_by_post_id(10)


def test_search_for_posts():
    posts = search_for_posts("квадратная")
    assert type(posts) == list, "Возвращается не список"
    assert len(posts) > 0, "Существующий пост не находится"
    assert "квадратная" in posts[0]["content"].lower(), "В найденном посте нет ключевого слова"
    assert set(posts[0].keys()) == keys_should_be_posts, "Неверный список ключей"


def test_get_post_by_pk():
    post = get_post_by_pk(1)
    assert type(post) == dict, "Возвращается не словарь"
    assert post["pk"] == 1, "Возвращается пост с неверным pk"
    assert set(post.keys()) == keys_should_be_posts, "Неверный список ключей"
