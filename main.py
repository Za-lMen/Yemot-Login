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
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
