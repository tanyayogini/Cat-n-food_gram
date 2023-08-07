from flask import Blueprint, jsonify
from utils import get_posts_all, get_post_by_pk


api_posts = Blueprint("api_posts", __name__)


@api_posts.get("/api/posts/")
def get_posts_json():
    posts = get_posts_all()
    return jsonify(posts)


@api_posts.get("/api/posts/<int:post_id>/")
def get_single_post_json(post_id):
    post = get_post_by_pk(post_id)
    return jsonify(post)
