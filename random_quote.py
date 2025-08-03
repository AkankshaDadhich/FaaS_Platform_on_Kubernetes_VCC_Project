import random
import os
from flask import Flask, request, render_template

app = Flask(__name__)

def generate_random_quote():
    quotes = [
        "The only way to do great work is to love what you do. – Steve Jobs",
        "Innovation distinguishes between a leader and a follower. – Steve Jobs",
        "Your time is limited, don’t waste it living someone else’s life. – Steve Jobs",
        "Stay hungry, stay foolish. – Steve Jobs",
        "Don’t let the noise of other’s opinions drown out your own inner voice. – Steve Jobs",
        "The journey of a thousand miles begins with one step. – Lao Tzu",
        "The only impossible journey is the one you never begin. – Tony Robbins",
        "Believe you can and you’re halfway there. – Theodore Roosevelt",
        "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill"
    ]
    return random.choice(quotes)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return render_template("quote.html", quote=generate_random_quote())
    return render_template("form.html")

port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=port)
