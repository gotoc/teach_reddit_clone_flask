from app import db

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255))
  url = db.Column(db.String(255))
  votecount = db.Column(db.Integer, default=0)
  subreddit = db.Column(db.String(255))

  def __repr__(self):
    return '<Post %r: %s>' % (self.title, self.subreddit)

class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  post_id = db.Column(db.Integer)
  text = db.Column(db.String(255))

  def __repr__(self):
    return '<Comment %r: %s>' % (self.text, self.post_id)