from flask import Flask

app = None

def create_app():
    global app
    
    if not app:
        app = Flask(__name__)
    return app