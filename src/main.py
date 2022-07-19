from datetime import datetime
from fastapi import FastAPI
from dataclasses import dataclass
from enum import Enum
import pydantic


class Models(Enum):
    alexnet = "alexnet"
    resnet = "resnset"
    lenet = "lenet"


class Item(pydantic.BaseModel):
    name: str
    id: int


@dataclass
class Post:
    id: int
    title: str
    content: str


@dataclass
class Author:
    id: int
    first_name: str
    last_name: str


app = FastAPI()

posts = {1: Post(id=1, title="first post", content="This is the first post!")}
authors = {1: Author(id=1, first_name="Homayoon", last_name="Alimohammadi")}


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI web api!"}


@app.get("/test")
def test(test_var: bool = False):
    return test_var


@app.post("/items/")
def create_item(item: Item):
    return {"creation_date": datetime.now(), **item.dict()}


@app.get("/models/{model_name}")
def get_model_list(model_name: Models):
    print(model_name, type(model_name))
    print(model_name.value)
    return model_name, model_name.value


@app.get("/files/{file_path:path}")
def get_file(file_path: str):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError as e:
        return e.strerror


@app.get("/posts/")
def get_post_list():
    return posts


@app.post("/posts/")
def create_post(post: Post):
    return post.dict()


@app.get("/authors/")
def get_author_list():
    return authors


@app.get("/posts/{post_id}")
def get_post_details(post_id: int):
    return posts.get(post_id)


@app.get("/authors/{author_id}")
def get_author_details(author_id: int):
    return authors.get(author_id)
