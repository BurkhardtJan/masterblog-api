from flask import Flask, jsonify, request
from flask_cors import CORS
from blog_post_handler import BlogPost

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]
blog_posts = BlogPost("posts.json")


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Returns blog posts as json"""
    posts_data = blog_posts.posts
    return jsonify(posts_data)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Adds a new post to the database."""
    json_data = request.get_json()
    if not "title" in json_data and not "content" in json_data:
        return jsonify({"error": "title and content are required"}), 400
    elif not "title" in json_data:
        return jsonify({"error": "title is required"}), 400
    elif not "content" in json_data:
        return jsonify({"error": "content is required"}), 400
    title = json_data["title"]
    content = json_data["content"]
    if title == "" and content == "":
        return jsonify({"error": "title and content are required"}), 400
    elif title == "":
        return jsonify({"error": "title is required"}), 400
    elif content == "":
        return jsonify({"error": "content is required"}), 400
    new_post = blog_posts.add(title, content)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete(post_id):
    """Delete a blog post by ID"""
    post_to_delete = blog_posts.fetch_post_by_id(post_id)
    if not post_to_delete:
        return jsonify({"error": f"post with id {post_id} not found"}), 404
    blog_posts.delete(post_id)
    message = {
        "message": f"Post with id {post_id} has been deleted successfully."
    }
    return jsonify(message), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update(post_id):
    """Updates a blog post by ID"""
    post_to_update = blog_posts.fetch_post_by_id(post_id)
    json_data = request.get_json()
    if not post_to_update:
        return jsonify({"error": f"post with id {post_id} not found"}), 404
    if "title" in json_data:
        title = json_data["title"]
    else:
        title = post_to_update["title"]
    if "content" in json_data:
        content = json_data["content"]
    else:
        content = post_to_update["content"]
    blog_posts.change(post_id, title, content)
    message = {
        "id": post_id,
        "title": title,
        "content": content
    }
    return jsonify(message), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Searches and returns matching blog posts as json"""
    title = request.args.get("title")
    content = request.args.get("content")
    title = title if title is not None else ""
    content = content if content is not None else ""
    posts = blog_posts.search_posts(title, content)
    return jsonify(posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
