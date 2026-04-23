import json
import os
from datetime import datetime

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

    def add(self, title, content, author="Anonym", date=datetime.today().strftime('%Y-%m-%d')):
        """Adds and saves blog post. Sets id to max(id)+1"""
        new_id = max([p['id'] for p in self._posts], default=0) + 1

        new_post = {
            "id": new_id,
            "title": title,
            "content": content,
            "author": author,
            "date": date,
            "likes": 0,

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

    def change(self, post_id, title, content, author = "Anonym", date=datetime.today().strftime('%Y-%m-%d')):
        """Changes blog post with selected id."""
        changed_post = {
            "id": post_id,
            "title": title,
            "content": content,
            "author": author,
            "date": date,
            "likes": 0,
        }
        post_index = self.fetch_post_position_by_id(post_id)
        self._posts[post_index] = changed_post
        self._save_data()

    def search_posts(self, title, content, author, date):
        """Searches blog posts with selected title and content."""
        found = []
        for post in self.posts:
            if title in post['title'] and content in post['content'] and author in post['author'] and date in post['date']:
                found.append(post)
        return found

    def sorted(self, sort, direction):
        """Sorts blog posts according to specified sort."""
        if direction == "desc":
            reverse = True
        else:
            reverse = False
        sorted_posts = sorted(self._posts, key=lambda p: p[sort], reverse=reverse)
        return sorted_posts

    def like(self, post_id):
        """Likes blog post with selected id."""
        post_index = self.fetch_post_position_by_id(post_id)
        self._posts[post_index]['likes'] += 1
        self._save_data()
