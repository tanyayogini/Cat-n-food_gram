import json


def load_json(path: str) -> list:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_posts_all() -> list:
    posts = load_json("data/posts.json")
    return posts


def get_posts_by_user(user_name: str) -> list:
    posts = get_posts_all()
    posts_by_user = []
    user_existed = False

    for post in posts:
        if post["poster_name"].lower() == user_name.lower():
            posts_by_user.append(post)
            user_existed = True

    if not user_existed:
        raise ValueError("User not found")

    return posts_by_user


def get_comments_by_post_id(post_id: int) -> list:
    posts = load_json("data/posts.json")
    comments = load_json("data/comments.json")
    comments_by_post_id = []

    post_existed = False
    for post in posts:
        if post["pk"] == post_id:
            post_existed = True

    if not post_existed:
        raise ValueError("Post not found")

    for comment in comments:
        if comment["post_id"] == post_id:
            comments_by_post_id.append(comment)

    return comments_by_post_id


def search_for_posts(query: str) -> list:
    posts = get_posts_all()
    posts_by_query = []
    number_posts = 0

    for post in posts:
        if query.lower() in post["content"].lower():
            posts_by_query.append(post)
            number_posts += 1

        if number_posts == 10:
            break

    return posts_by_query


def get_post_by_pk(pk: int) -> dict:
    posts = get_posts_all()

    for post in posts:
        if post["pk"] == pk:
            return post


def add_tags_to_post(post: dict) -> dict:
    """Получает пост в формате словаря. Для поста в тексте превращает слова, начинающиеся с #
    в ссылку по соответствующему тегу. Возвращает пост в формате словаря"""
    post_words = post["content"].split(" ")
    for index, word in enumerate(post_words):
        if word[0] == "#":
            post_words[index] = f'<a href="/tag/{word[1:]}">{word}</a>'

    post["content"] = " ".join(post_words)
    return post


def add_tags_to_list_posts(posts: list) -> list:
    """Получает список постов. В каждом посте в тексте превращает слова,
    начинающиеся на # в ссылку по соответствующему тегу. Возвращает список постов"""
    for post in posts:
        post = add_tags_to_post(post)

    return posts


def search_post_by_tag(tag_name: str) -> list:
    posts = get_posts_all()
    post_with_tag = []
    for post in posts:
        post_words = post["content"].split(" ")
        for word in post_words:
            if f"#{tag_name}" == word:
                post_with_tag.append(post)
                break

    return post_with_tag


def get_bookmarks_all() -> list:
    bookmarks_posts = load_json("data/bookmarks.json")
    return bookmarks_posts


def add_bookmarks_to_json(post_id: int) -> None:
    bookmarks_posts = get_bookmarks_all()
    posts = get_posts_all()
    for post in posts:
        if post["pk"] == post_id:
            bookmarks_posts.append(post)
            break

    with open("data/bookmarks.json", "w", encoding="utf-8") as file:
        json.dump(bookmarks_posts, file)


def remove_bookmarks_to_json(post_id: int) -> None:
    bookmarks_posts = get_bookmarks_all()
    posts = get_posts_all()
    for post in posts:
        if post["pk"] == post_id:
            bookmarks_posts.remove(post)
            break

    with open("data/bookmarks.json", "w", encoding="utf-8") as file:
        json.dump(bookmarks_posts, file)
