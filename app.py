from flask import Flask as fls,request as req,render_template as renplate,session
from werkzeug.security import generate_password_hash,check_password_hash
from flaskext.mysql import MySQL
from markupsafe import escape as esc # variable rules in flask
from flask.helpers import url_for
import json
from werkzeug.utils import redirect

app = fls(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root1234'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

app.secret_key = "sdajkdhkasds"

#using session =>  get_flashed_messages()
@app.route('/')
def index():
    return renplate('index.html')

@app.route('/signup')
def showSignUp():
    return renplate('signup.html')

@app.route('/signupProcess',methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = req.form['inputName']
    _email = req.form['inputEmail']
    _password = req.form['inputPassword']
    _hashed_password = generate_password_hash(_password,method='sha256',salt_length=8)
    cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
    data = cursor.fetchall()
    # validate the received values
    if len(data) == 0:
        conn.commit()
        return json.dumps({'data':[{'nama':f'{_name}','email':f'{_email}','pass':f'{_hashed_password}'}]})
    else:
        return json.dumps({'html':'Username Exist'})

@app.route('/signin')
def showSignin():
    try :
        session['name']
    except:
        return renplate('signin.html')
    else:
        return redirect('/')

@app.route('/signinProcess',methods=['POST'])
def signIn():
    # read the posted values from the UI
    _email = req.form['inputEmail']
    _password = req.form['inputPassword']
    _hashed_password = generate_password_hash(_password,method='sha256',salt_length=8)
    cursor.execute(f"SELECT * FROM tbl_user WHERE user_username = '{_email}' ")
    data = cursor.fetchall()
    # validate the received values
    if len(data) > 0:
        if check_password_hash(data[0][3],_password):
            session['name'] = data[0][1]
            return esc(session['name'])
        else:
            return json.dumps({'data':'Login totally Failed'})
    else:
        return json.dumps({'data':'not available'})

@app.route('/logoutProcess')
def logout():
    session.pop('name',None)
    return redirect('/')