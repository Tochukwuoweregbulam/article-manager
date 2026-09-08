from fastapi import APIRouter, Depends, HTTPException, status

from api.core.security import (
    get_current_user,
    get_current_admin
)

from api.core.response import success_response

from api.v1.schemas.post import PostCreate

from api.v1.services.post import (
    get_all_posts,
    get_latest_post,
    get_post_by_id,
    create_post,
    delete_post
)


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# GET ALL POSTS
@router.get("/")
def get_posts():

    posts = get_all_posts()

    return success_response(
        data=posts,
        message="Posts fetched successfully"
    )


# GET LATEST POST
@router.get("/latest")
def find_latest_post():

    post = get_latest_post()

    return success_response(
        data=post,
        message="Latest post fetched successfully"
    )


# GET POST BY ID
@router.get("/{id}")
def get_post(id: int):

    post = get_post_by_id(id)

    if post is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return success_response(
        data=post,
        message="Post fetched successfully"
    )


# CREATE POST
@router.post("/")
def create_posts(
    model: PostCreate,
    # current_user: dict = Depends(get_current_user)
):

    new_post = create_post(
        model.title,
        model.content
    )

    return success_response(
        data=new_post,
        message="Post created successfully",
        status_code=status.HTTP_201_CREATED
    )


# DELETE POST
@router.delete("/{id}")
def remove_post(
    id: int,
    current_admin: dict = Depends(get_current_admin)
):

    deleted_post = delete_post(id)

    if deleted_post is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return success_response(
        data=deleted_post,
        message="Post deleted successfully"
    )