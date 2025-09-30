from flask import Flask, request
import os
app = Flask(__name__)
@app.route('/')
def reverse_text():
    # קבל את הפרמטר 'text' מה-URL (למשל, ?text=hello)
    text = request.args.get('text', 'No text provided')
    # החזר את הטקסט הפוך
    reversed_text = text[::-1]
    return f'Reversed text: {reversed_text}'
