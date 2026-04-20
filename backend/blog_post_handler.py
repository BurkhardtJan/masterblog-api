import json
import os


class BlogPost:
    """Manage blog posts in JSON."""

    def __init__(self, filename):
        self.filename = filename
        self._posts = self._load_data()

    def _load_data(self):
        """Reads data from file or returns empty"""
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self):
        """Saves data into in JSON."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self._posts, f, indent=4)

    @property
    def posts(self):
        """Returns list of blog posts."""
        return self._posts

    def add(self, title, content):
        """Adds and saves blog post. Sets id to max(id)+1"""
        new_id = max([p['id'] for p in self._posts], default=0) + 1

        new_post = {
            "id": new_id,
            "title": title,
            "content": content,
        }
        self._posts.append(new_post)
        self._save_data()
        return new_post

    def delete(self, post_id):
        """Deletes post with selected number."""
        self._posts = [p for p in self._posts if p['id'] != post_id]
        self._save_data()

    def fetch_post_by_id(self, post_id):
        """Fetches blog post with selected id."""
        for post in self._posts:
            if post['id'] == post_id:
                return post
        return None

    def fetch_post_position_by_id(self, post_id):
        """Fetches blog post position with selected id."""
        i = 0
        for post in self._posts:
            if post['id'] == post_id:
                return i
            i += 1
        return None

    def change(self, post_id, title, content):
        """Changes blog post with selected id."""
        changed_post = {
            "id": post_id,
            "title": title,
            "content": content
        }
        post_index = self.fetch_post_position_by_id(post_id)
        self._posts[post_index] = changed_post
        self._save_data()

