from flask.ext.wtf import Form
from wtforms import StringField

class CreatePostForm(Form):
  title       = StringField('title')
  url         = StringField('url')
  subreddit   = StringField('subreddit')

class PostCommentForm(Form):
  text = StringField('comment')