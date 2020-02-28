from flask import Flask, request
from main import wine

app = Flask("functions")
methods = ["GET", "POST", "PUT", "DELETE"]

@app.route("/wine" , methods=methods)
@app.route("/wine/<id>" , methods=methods)

def catch_all(id=""):
    request.path = "/" + id
    return wine(request)

if __name__ =="__main__":
    app.run()
