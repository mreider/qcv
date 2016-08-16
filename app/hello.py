""" hello.py """
import json
import traceback
import datetime
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
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
    user_id = db.Column(db.Unicode(50),primary_key=True)
    first_name = db.Column(db.Unicode(100))
    last_name = db.Column(db.Unicode(100))
    maiden_name = db.Column(db.Unicode(100))
    formatted_name = db.Column(db.Unicode(100))
    phonetic_first_name = db.Column(db.Unicode(100))
    phonetic_last_name = db.Column(db.Unicode(100))
    formatted_phonetic_name = db.Column(db.Unicode(100))
    headline = db.Column(db.Unicode(100))
    location = db.Column(db.Unicode(50))
    industry = db.Column(db.Unicode(50))
    current_share = db.Column(db.Unicode(50))
    num_connections = db.Column(db.Integer)
    num_connections_capped = db.Column(db.Boolean)
    summary = db.Column(db.Unicode(1000))
    specialties = db.Column(db.Unicode(1000))
    picture_url = db.Column(db.Unicode(250))
    public_profile_url = db.Column(db.Unicode(250))


class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Unicode(50),ForeignKey("user_profile.user_id"))
    school_name = db.Column(db.Unicode(100))
    field_of_study = db.Column(db.Unicode(200))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    degree = db.Column(db.Unicode(100))
    activities = db.Column(db.Unicode(2500))
    notes = db.Column(db.Unicode(2500))

class Certifications(db.Model):
    __tablename__ = 'certifications'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Unicode(50),ForeignKey("user_profile.user_id"))
    name = db.Column(db.Unicode(2500))
    authority = db.Column(db.Unicode(2500))
    number = db.Column(db.Unicode(500))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

class Positions(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Unicode(50),ForeignKey("user_profile.user_id"))
    title = db.Column(db.Unicode(100))
    summary = db.Column(db.Unicode(1000))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_current  = db.Column(db.Boolean)
    company = db.Column(db.Unicode(1000))


linked_in_url = 'https://www.linkedin.com/oauth/v2/authorization'

@app.route('/sync',methods=['GET','POST'])
def sync():
    token = session['access_token']
    profile_url = 'https://api.linkedin.com/v1/people/~:(id,first-name,last-name,headline,picture-url,industry,summary,specialties,positions:(id,title,summary,start-date,end-date,is-current,company:(id,name,type,size,industry,ticker)),educations:(id,school-name,field-of-study,start-date,end-date,degree,activities,notes),associations,interests,num-recommenders,date-of-birth,publications:(id,title,publisher:(name),authors:(id,name),date,url,summary),languages:(id,language:(name),proficiency:(level,name)),skills:(id,skill:(name)),certifications:(id,name,authority:(name),number,start-date,end-date),courses:(id,name,number),recommendations-received:(id,recommendation-type,recommendation-text,recommender),honors-awards,three-current-positions,three-past-positions,volunteer)?oauth2_access_token='+token+'&format=json'
    print profile_url
    response = requests.get(profile_url)

    print response.status_code
    if response.status_code == 200:
        data = json.loads(response.text)

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
    print 'On Dev ? %s'%SETTINGS['ON_DEV']

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

