""" hello.py """
import json
import traceback
import datetime
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
import requests
from config import SETTINGS
from uuid import uuid4

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://'+SETTINGS['DB_USER_NAME']+':'+SETTINGS['DB_USER_NAME']+'@'+\
                                    SETTINGS['DB_HOST']+'/'+SETTINGS['DB_NAME']
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    user_id = db.Column(db.Integer,primary_key=True)
    created = db.Column(db.DateTime,default=datetime.datetime.utcnow)

linked_in_url = 'https://www.linkedin.com/oauth/v2/authorization'

@app.route('/sync',methods=['GET','POST'])
def sync():
    return session['access_token']

@app.route('/callback',methods=['GET','POST'])
def auth_callback():
    code = request.args.get('code')
    if SETTINGS['ON_DEV']:
        callback_url = 'http://localhost:5000/callback'
    else:
        callback_url = 'http://qcv.space/callback'

    auth_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    grant_type = 'authorization_code'
    client_id = SETTINGS['LINKEDIN_CLIENT_ID']
    client_secret = SETTINGS['LINKEDIN_CLIENT_SECRET']

    params = {'code':code,'grant_type':grant_type,'redirect_uri':callback_url,'client_id':client_id,'client_secret':client_secret}

    response = requests.post(auth_url,data=params)
    print response.status_code
    if response.status_code == 200:
        content = json.loads(response.text)
        session['access_token'] = content.get('access_token')
        return render_template('home.html',access_token = session.get('acess_token'))
    else:
        return render_template('error.html')

@app.route('/login',methods=['GET','POST'])
def login():


    if SETTINGS['ON_DEV']:
        callback_url = 'http://localhost:5000/callback'
    else:
        callback_url = 'http://qcv.space/callback'
    code = str(uuid4).replace('-','')
    print code
    url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id='+SETTINGS['LINKEDIN_CLIENT_ID']+'&redirect_uri='+callback_url+'&state='+code+'&scope=r_basicprofile'
    return redirect(url,code=302)

@app.route('/logout',methods=['GET','POST'])
def logout():
    del session['access_token']
    return redirect('/')

@app.route('/')
def hello():
    if session.get('access_token'):
        return render_template('home.html',access_token = session.get('acess_token'))
    else:
        return render_template('index.html')


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0',debug=True)
