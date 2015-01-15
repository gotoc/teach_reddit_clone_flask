from flask import render_template, redirect, request
from app import app, models, db
from .forms import CreatePostForm, PostCommentForm

@app.route('/')
@app.route('/home')
def index():
  posts = models.Post.query.all()
  posts = sorted(posts, key=lambda p: p.votecount, reverse=True)
  return render_template('index.html', posts=posts)

@app.route('/r/<subreddit>')
def subreddit(subreddit):
  posts = models.Post.query.filter(models.Post.subreddit == subreddit).all()
  posts = sorted(posts, key=lambda p: p.votecount, reverse=True)
  return render_template('index.html', posts=posts)

@app.route('/r/<subreddit>/<pid>', methods=['GET', 'POST'])
def post(subreddit, pid):
  form = PostCommentForm(request.form)
  post = models.Post.query.filter(models.Post.id == pid).one()
  comments = models.Comment.query.filter(models.Comment.post_id == pid).all()
  if request.method == 'POST':
    comment = models.Comment(post_id=pid, text=form.text.data)
    db.session.add(comment)
    db.session.commit()
    return redirect('/r/%s/%s' % (subreddit, pid))
  return render_template('post.html', form=form, post=post, comments=comments)

@app.route('/create_post', methods=['GET', 'POST'])
def create():
  form = CreatePostForm(request.form)
  if request.method == 'POST':
    post = models.Post(title=form.title.data, url=form.url.data, subreddit=form.subreddit.data)
    db.session.add(post)
    db.session.commit()
    return redirect('/home')
  return render_template('create_post.html', form=form)

@app.route('/clear', methods=['GET'])
def clear():
  post = models.Post.query.delete()
  db.session.commit()
  return redirect('/home')

@app.route('/vote', methods=['POST'])
def vote():
  pid = request.form['id']
  direction = request.form['direction']
  post = models.Post.query.filter(models.Post.id == pid).one()
  if direction == 'up':
    post.votecount += 1
  elif direction == 'down':
    post.votecount -= 1
  else:
    pass
  db.session.commit()
  return str(post.votecount)