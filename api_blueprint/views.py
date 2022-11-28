from flask import Blueprint, jsonify
import logging
from utils import get_posts_all, get_post_by_pk

# Подключаем логирование в нужном формате
logging.basicConfig(filename="logs/api.log", format="%(asctime)s [%(levelname)s] %(message)s")

# блюпринт для API
api_posts = Blueprint("api_posts", __name__)


# передает все посты в формате json
@api_posts.get("/api/posts/")
def get_posts_json():
    posts = get_posts_all()
    return jsonify(posts)


# передает пост по id в формате json
@api_posts.get("/api/posts/<int:post_id>/")
def get_single_post_json(post_id):
    post = get_post_by_pk(post_id)
    return jsonify(post)
