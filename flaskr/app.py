import os
import random

from flask import Flask, render_template
from ascii_art import read_in_art


app = Flask(__name__)

@app.route('/')
def index():
    return 'MDST Webscraping project!'


@app.route('/wordsearch/')
def wordsearch():
    wordrow = [chr(ord('a')+ x) * 20 for x in range(5)]
    return render_template('ctf.html', wordrow=wordrow)

@app.route('/caesar/')
def caesar_scrape():
    with open('static/caesar.txt', 'r') as f:
        lines = f.readlines()
        
    return render_template('caesar.html',word_caesar=zip(lines[:len(lines)//2], lines[len(lines)//2:]))

@app.route('/art/')
def art_index():
    messages=[
        'url: /art/<art>/',
        '<art> can be "elephant", "dogs", "beaver", or "tweetie"'
        ]
    
    return render_template('not_found.html', messages=messages)

@app.route('/shuffled_art/<art>/')
def unshuffled_ascii_art(art):
    lines = read_in_art(f'static/{art}.txt')
    ind_lines = [(ind, l) for ind, l in enumerate(lines)]

    random.shuffle(ind_lines)
    return render_template('ascii_shuffled.html', art=art, lines=ind_lines)

@app.route('/art/<art>/')
def ascii_art(art):
    lines = read_in_art(f'static/{art}.txt', replace=False)

    # random.shuffle(ind_lines)
    return render_template('ascii_art.html', art=art, line=''.join(lines))
    
if __name__ == '__main__':
    app.run()