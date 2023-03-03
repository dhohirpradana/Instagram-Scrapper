import os
from sys import stderr

from flask import Flask, jsonify, request
# from flask_cors import CORS

from ig_scrapper_scroll import handler as ig_scrapper_scroll_handler

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask</h2>'

@app.route('/instagram_scraper_scroll', methods=['POST'])
def instagram_scraper_scroll():
    return ig_scrapper_scroll_handler(request, jsonify)

if __name__ == "__main__":
    app.run(debug=True)