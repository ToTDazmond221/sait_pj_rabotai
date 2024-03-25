
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_data():
    if os.path.exists('forum_data.json'):
        with open('forum_data.json', 'r') as file:
            data = json.load(file)
    else:
        data = {'posts': []}
    return data

def save_data(data):
    with open('forum_data.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', posts=data['posts'])

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        data = load_data()
        post_content = request.form['content']
        post = {'content': post_content, 'comments': []}
        data['posts'].append(post)
        save_data(data)
        return redirect(url_for('index'))
    return render_template('add_post.html')

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    data = load_data()
    post = data['posts'][post_id-1]
    if request.method == 'POST':
        comment_content = request.form['content']
        comment = {'content': comment_content}
        post['comments'].append(comment)
        save_data(data)
        return redirect(url_for('view_post', post_id=post_id))
    return render_template('view_post.html', post=post, post_id=post_id)

@app.route('/post/<int:post_id>/answers', methods=['GET'])
def view_post_answers(post_id):
    data = load_data()
    post = data['posts'][post_id-1]
    return render_template('post_answers.html', comments=post['comments'])

@app.route('/post/<int:post_id>/details', methods=['GET'])
def view_post_details(post_id):
    data = load_data()
    post = data['posts'][post_id-1]
    return render_template('view_post.html', post=post, post_id=post_id)

if __name__ == '__main__':
    app.run(debug=True)
