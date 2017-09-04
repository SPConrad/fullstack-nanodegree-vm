# "Database code" for the DB Forum.
import psycopg2
import datetime
import bleach

POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  """Return all posts from the 'database', most recent first."""
  DB = psycopg2.connect("dbname=forum")
  c = DB.cursor()
  c.execute("select content, time from posts order by time desc")
  posts = c.fetchall()
  DB.close()
  return posts

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  DB = psycopg2.connect("dbname=forum")
  c = DB.cursor()
  bleach.clean(content)
  c.execute("INSERT INTO posts (content) VALUES (%s)", (content,))
  DB.commit()
  DB.close()


