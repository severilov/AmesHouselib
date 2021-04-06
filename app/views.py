# !/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
import subprocess

app = Flask(__name__)

from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/train')
def train():
    ps = subprocess.run(["python", "./src/scripts/train.py"], capture_output=True)
    return ps.stdout


@app.route('/test')
def test():
    ps = subprocess.run(["python", "./src/scripts/test.py"], capture_output=True)
    return ps.stdout


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
