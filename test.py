from flask import Flask as fls,request as req,render_template as renplate
from markupsafe import escape as esc # variable rules in flask
from flask.helpers import url_for

# You can add variable sections to a URL by marking sections with <variable_name>. 
# Your function then receives the <variable_name> as a keyword argument. Optionally, 
# you can use a converter to specify the type of the argument like <converter:variable_name>.

#>>>unique URL's

# The canonical URL for the "home" endpoint has a trailing slash. 
# It’s similar to a folder in a file system. If you access the URL without a trailing slash, 
# Flask redirects you to the canonical URL with the trailing slash.

# The canonical URL for the "index" endpoint does not have a trailing slash. 
# It’s similar to the pathname of a file. Accessing the URL with a trailing 
# slash produces a 404 “Not Found” error. This helps keep URLs unique for these resources, 
# which helps search engines avoid indexing the same page twice.

#>>>

app = fls(__name__)



@app.route('/')
def index():
    return 'index'

@app.route('/home/')
def home():
    return 'home'

@app.route('/user/<username>')
def show_user_profile(username):
    return f'User : {esc(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post : {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {esc(subpath)}'

#CONVERTER TYPES
# string =>(default) accepts any text without a slash
# int => accepts positive integers
# float => accepts positive floating point values
# path => like string but also accepts slashes
# uuid => accepts UUID strings

#>>>HTTP Methods
@app.route('/login', methods=['GET','POST'])
def login():
    if req.method == 'POST':
        return 'l'
    else:
        return '1'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('show_user_profile', username='John Doe'))

