from datetime import datetime
from fastapi import Body, FastAPI, Path, Query
from dataclasses import dataclass
from enum import Enum
import pydantic


class Models(Enum):
    alexnet = "alexnet"
    resnet = "resnset"
    lenet = "lenet"


class Image(pydantic.BaseModel):
    url: pydantic.HttpUrl
    name: str

    class Config:
        schema_extra = {
            "example": {
                "url": "https://target.website.com/path/to/image",
                "name": "that same kitty again!",
            }
        }


class Item(pydantic.BaseModel):
    name: str
    id: int = pydantic.Field(ge=1, title="ID of an Item.")
    image: Image | None = None


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
def create_item(
    item: Item = Body(
        examples={
            "normal": {
                "summary": "acceptable example",
                "description": "this is how a true Item should look like!",
                "value": {
                    "item": {
                        "name": "nice item",
                        "id": "10",
                        "image": {
                            "url": "https://www.images.com/path/to/image",
                            "name": "nice image",
                        },
                    }
                },
            },
            "bad": {
                "summary": "a bad example",
                "description": "this is how a bad Item should look like!",
                "value": {
                    "item": {
                        "name": "a;lsgjsdlfj",
                        "id": "-10",
                        "image": {
                            "url": "a;dlkfja or /path/to/image alone",
                            "name": "aflaksdjfl",
                        },
                    }
                },
            },
        },
    )
):
    return {"creation_date": datetime.now(), **item.dict()}


@app.get("/greet/")
async def greet(name: str | None = Query(default=None, max_length=10)):
    if name:
        return f"Greetings {name}!"
    return "Greetings!"


# if you want to declare a query parameter of type "list",
# you should use "Query". Otherwise it will be considered a request body.
# Because only singular types are primarily considered a query parameter.
@app.get("/greets/")
async def greets(names: list[str] | None = Query(default=None)):
    if names:
        names = ", ".join(names)
        return f"Greetings {names}!"
    return "Greetings!"


@app.get("/say-hello/")
async def say_hello(
    name: str = Query(
        default="dear nooshin joon",
        title="User Name",
        alias="user-name",
        deprecated=True,
        min_length=3,
        max_length=20,
        regex="nooshin",
    )
):
    return f"Hello {name}"


@app.get("/items/{item_id}")
async def get_item_by_id(
    item_id: int = Path(title="ID of the item", ge=1, lt=3),
    q: str = Query(default="something", max_length=20),
):
    items = {1: "item 1", 2: "item 2"}
    return [items[item_id], q]


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
def create_post(post: Post = Body(embed=True)):
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
