from flask import Flask, render_template, request, jsonify, redirect
from api_blueprint.views import api_posts
from werkzeug.exceptions import HTTPException

from utils import *

app = Flask(__name__)
app.config['app.json.ensure_ascii'] = False
app.register_blueprint(api_posts)


# Главная страница, выведем все посты; перед передачей в шаблон, добавим ссылки по тегам
@app.route("/")
def main_page():
    posts = add_tags_to_list_posts(get_posts_all())

    # для вывода на главной странице количества сохраненных постов, загрузим закладки и передадим
    # в шаблон их количество
    bookmarks_posts = get_bookmarks_all()
    number_bookmarks = len(bookmarks_posts)

    return render_template("index.html", posts=posts, number_bookmarks=number_bookmarks)


# страница отдельного поста; перед передачей в шаблон добавим ссылки по тегам;
@app.get("/posts/<int:post_id>/")
def single_post_page(post_id):
    post = add_tags_to_post(get_post_by_pk(post_id))

    # загрузим комментарии, определим их количество и все передадим в шаблон
    comments = get_comments_by_post_id(post_id)
    number_comments = len(comments)
    return render_template("post.html", **post, comments=comments, number_comments=number_comments)


# страница поиска по запросу
@app.get("/search")
def search_page():
    query = request.args.get("s")

    # загрузим посты, добавим ссылки по тегам, определим количество найденных постов и все передадим
    # в шаблон
    posts_by_query = add_tags_to_list_posts(search_for_posts(query))
    number_posts = len(posts_by_query)
    return render_template("search.html", posts_by_query=posts_by_query, number_posts=number_posts)


# страница со всеми постами одного пользователя
@app.get("/users/<user_name>")
def user_page(user_name):
    posts_by_user = add_tags_to_list_posts(get_posts_by_user(user_name))
    return render_template("user-feed.html", user_name=user_name, posts_by_user=posts_by_user)


# страница по тегу
@app.get("/tag/<tag_name>")
def tag_page(tag_name):
    posts_by_tag = add_tags_to_list_posts(search_post_by_tag(tag_name))
    return render_template("tag.html", tag_name=tag_name, posts_by_tag=posts_by_tag)


# добавление поста в закладки
@app.get("/bookmarks/add/<int:post_id>")
def add_bookmark_page(post_id):
    add_bookmarks_to_json(post_id)
    return redirect("/", code=302)


# удаление поста из закладок
@app.get("/bookmarks/remove/<int:post_id>")
def remove_bookmark_page(post_id):
    remove_bookmarks_to_json(post_id)
    return redirect("/", code=302)


# страница закладок
@app.get("/bookmarks/")
def bookmarks_page():
    bookmarks_posts = add_tags_to_list_posts(get_bookmarks_all())
    return render_template("bookmarks.html", bookmarks_posts=bookmarks_posts)


# обработка ошибок
@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    return f"статус-код {response.status_code}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=25000)
