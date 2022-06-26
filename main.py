from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel


app = FastAPI()


########## Post Model ##########
class PostValidData(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


########## Post Data ##########
my_posts = [{
    "title": "Teste de titulo!",
    "content": "El mejor post de todos",
    "published": True,
    "rating": 5,
    "id": 0
},
    {
    "title": "Post regular!",
    "content": "Un post no tan bueno",
    "published": True,
    "rating": 4,
    "id": 1
},
    {
    "title": "Mal post",
    "content": "Un post malo",
    "published": True,
    "rating": 2,
    "id": 2
}]


########## Logic functions ##########
def find_post_by_id(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_post_index_by_id(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index


########## Api requests ##########
@app.get("/")
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    data = {
        "posts": my_posts
    }
    return data


@app.get("/posts/{id}")
def get_post(id: int):
    post_data = find_post_by_id(id)
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"POST WITH ID: {id} WAS NOT FOUND. ERROR {status.HTTP_404_NOT_FOUND}")
    data = {
        "post details": post_data
    }
    return data


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_post_index_by_id(id)
    if not post_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"POST WITH ID: {id} WAS NOT FOUND. ERROR {status.HTTP_404_NOT_FOUND}")
    my_posts.pop(post_index)
    data = Response(status_code=status.HTTP_204_NO_CONTENT)
    return data


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostValidData):
    post_data = post.dict()
    post_data["id"] = randrange(1, 1000000000)
    my_posts.append(post_data)
    succes = {
        "message": "Succesfully created post",
        "data": post_data
    }
    return succes


@app.put("/posts/{id}")
def update_post(id: int, updated_post_data: PostValidData):
    post_index = find_post_index_by_id(id)
    if not post_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"POST WITH ID: {id} WAS NOT FOUND. ERROR {status.HTTP_404_NOT_FOUND}")
    post_dic = updated_post_data.dict()
    post_dic['id'] = id
    my_posts[post_index] = post_dic
    post_updated = {
        "message": "Post succesfully updated",
        "data": post_dic
    }
    return post_updated
