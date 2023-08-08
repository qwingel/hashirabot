from flask import Blueprint, request, session

module = Blueprint("main", __name__, url_prefix="/")


@module.post("/")
def index():
    data = request.get_json()
    print(data["login"])
    return "Success! =)"