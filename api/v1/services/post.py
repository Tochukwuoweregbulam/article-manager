from random import randrange

from api.db.database import My_post


def get_all_posts():

    return My_post


def get_latest_post():

    return My_post[-1]


def get_post_by_id(post_id: int):

    for post in My_post:

        if post["id"] == post_id:
            return post

    return None


def create_post(title: str, content: str):

    post = {
        "title": title,
        "content": content,
        "id": randrange(2, 1000000)
    }

    My_post.append(post)

    return post


def delete_post(post_id: int):

    for index, post in enumerate(My_post):

        if post["id"] == post_id:

            return My_post.pop(index)

    return None