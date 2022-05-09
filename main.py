from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_post():
    post = {
        "data": "This is your post"
    }
    return post


@app.post("/create_post")
def create_post(post_data: dict = Body(...)):
    succes = {
        "message": "Succesfully created post",
        "data": post_data
    }
    return succes
