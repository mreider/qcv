""" hello.py """
import json
import traceback
import datetime
from flask import Flask, render_template, request, session, Response, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from weasyprint import HTML, CSS
from werkzeug.utils import redirect
import requests
from config import SETTINGS
from uuid import uuid4
import os

from bs4 import BeautifulSoup
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

class Themes(db.Model):
    __tablename__ = 'themes'
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.Unicode(100))
    last_name = db.Column(db.Unicode(100))
    html_content = db.Column(db.Text)
    css_content = db.Column(db.Text)

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

def update_user(data):
    user_id = data.get('id')
    try:
        print 'USer ID %s'%user_id
        if user_id:
            user = UserProfile.query.get(user_id)
            if user:
                user.first_name = data.get('firstName')
                user.last_name = data.get('lastName')
                user.industry = data.get('industry')
                user.headline = data.get('headline')
                user.picture_url = data.get('pictureUrl')
                user.summary = data.get('summary')
            else:
                user = UserProfile(user_id=user_id,first_name=data.get('firstName'),last_name=data.get('lastName'),
                                   industry=data.get('industry'),headline=data.get('headline'),
                                   picture_url = data.get('pictureUrl'),summary = data.get('summary'))
                db.session.add(user)
            db.session.commit()
            update_positions(data,user)
            update_education(data,user)
            update_certifications(data,user)

        db.session.commit()
    except:
        traceback.print_exc()
        db.session.rollback()
def update_certifications(data,user):
    if data.get('certifications'):
        user_id = user.user_id
        for cert in data.get('certifications').get('values'):
            cert_id = cert.get('id')
            year = position.get('startDate').get('year')
            month = position.get('startDate').get('month')
            start_date = datetime.now().replace(year=year,month=month)
            year = position.get('endDate').get('year')
            month = position.get('startDate').get('month')
            end_date = datetime.now().replace(year=year,month=month)

            certification = Certifications.query.get(cert_id)
            if certification:
                certification.name = cert.get('name')
                certification.authority = cert.get('authority').get('name')
                certification.number = cert.get('number')
                certification.start_date = start_date
                certification.end_date = end_date
            else:
                certification = Certifications(id=cert_id,user_id=user_id,name=cert.get('name'),
                                              authority = cert.get('authority').get('name'),number = cert.get('number'),
                                              start_date = start_date,end_date = end_date)
            db.session.add(certification)

def update_education(data,user):
    if data.get('educations'):
        for edu in data.get('educations').get('values'):
            edu_id = edu.get('id')
            education = Education.query.get(edu_id)
            startYear = edu.get('startDate').get('year')
            start_year = datetime.now().replace(year=startYear)
            endYear = edu.get('endDate').get('year')
            end_year = datetime.now().replace(year=endYear)
            user_id = user.user_id
            if education:
                education.school_name = edu.get('schoolName')
                education.field_of_study = edu.get('fieldOfStudy')
                education.degree = edu.get('degree')
                education.start_date = start_year
                education.end_date = end_year
            else:
                education = Education(id=edu_id,user_id=user_id,school_name=edu.get('schoolName'),
                                      field_of_study = edu.get('fieldOfStudy'),degree = edu.get('degree'),
                                      start_date = start_year,end_date = end_year)
            db.session.add(education)


def update_positions(data,user):
    from datetime import datetime
    if data.get('positions'):
        for position in data.get('positions').get('values'):
            p_id = position.get('id')
            pos = Positions.query.get(p_id)
            month = position.get('startDate').get('month')
            year = position.get('startDate').get('year')
            start_date = datetime.now().replace(month=month,year=year)
            company  = position.get('company').get('name')
            is_current = position.get('isCurrent')
            end_date = None
            if not is_current:
                month = position.get('endDate').get('month')
                year = position.get('endDate').get('year')
                end_date = datetime.now().replace(month=month,year=year)

            if pos :
                pos.summary = position.get('summary')
                pos.title = position.get('title')
                pos.is_current = position.get('isCurrent')
                pos.start_date = start_date
                pos.company = company
                if end_date:
                    pos.end_date = end_date

            else:
                pos = Positions(id=p_id,summary=data.get('summary'),title=data.get('title'),is_current=data.get('isCurrent'),
                                start_date=start_date,company=company,end_date=end_date)
            pos.user_id = user.user_id
            db.session.add(pos)
    else:
        pass

@app.route('/sync',methods=['GET','POST'])
def sync():
    token = session['access_token']
    profile_url = 'https://api.linkedin.com/v1/people/~:(id,first-name,last-name,headline,picture-url,industry,summary,specialties,positions:(id,title,summary,start-date,end-date,is-current,company:(id,name,type,size,industry,ticker)),educations:(id,school-name,field-of-study,start-date,end-date,degree,activities,notes),associations,interests,num-recommenders,date-of-birth,publications:(id,title,publisher:(name),authors:(id,name),date,url,summary),languages:(id,language:(name),proficiency:(level,name)),skills:(id,skill:(name)),certifications:(id,name,authority:(name),number,start-date,end-date),courses:(id,name,number),recommendations-received:(id,recommendation-type,recommendation-text,recommender),honors-awards,three-current-positions,three-past-positions,volunteer)?oauth2_access_token='+token+'&format=json'
    print profile_url
    response = requests.get(profile_url)

    print response.status_code
    if response.status_code == 200:
        data = json.loads(response.text)
        print data
        update_user(data)
    return session['access_token']

@app.route('/pdf/<first_name>.<last_name>',methods=['GET'])
def pdf(first_name,last_name):

    theme = Themes.query.filter_by(first_name=first_name).filter_by(last_name=last_name).first()
    if theme:
        htmlcontent = theme.html_content
        css = theme.css_content
    user = UserProfile.query.filter_by(first_name=first_name).filter_by(last_name=last_name).first()
    if user:
        positions = Positions.query.filter_by(user_id=user.user_id).all()
        educations = Education.query.filter_by(user_id=user.user_id).all()
        certifications = Certifications.query.filter_by(user_id=user.user_id).all()
    if htmlcontent:
        content = render_template_string(htmlcontent,first_name=first_name,last_name=last_name,
                                       user=user,positions=positions,educations=educations,
                                        certifications=certifications)
        print 'Saved content'
    else:
        content = render_template('basictheme.html',
                                   user=user,positions=positions,educations=educations,
                                    certifications=certifications)

    data = render_template('resume.html',theme=content,themestyle=css,first_name=first_name,last_name=last_name)
    html = HTML(string=data)
    css_file = file('print.css','r')
    css_content = css_file.read()

    css_content = css_content % (first_name+'.'+last_name+'s CV')
    css = CSS(string=css_content)
    output_file = '/tmp/cv.pdf'
    if os.path.exists(output_file):
        os.remove(output_file)
    html.write_pdf(output_file,stylesheets=[css])
    content = file(output_file).read()
    print 'PDF Generated at %s'%output_file
    return Response(content,
                       mimetype="application/pdf",
                       headers={"Content-Disposition":
                                    "attachment;filename=resume.pdf"})

@app.route('/callback',methods=['GET','POST'])
def auth_callback():
    redirectto = session.get('redirect')
    code = request.args.get('code')
    callback_url = SETTINGS['URL_BASE']+'callback'
    auth_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    grant_type = 'authorization_code'
    client_id = SETTINGS['LINKEDIN_CLIENT_ID']
    client_secret = SETTINGS['LINKEDIN_CLIENT_SECRET']

    params = {'code':code,'grant_type':grant_type,'redirect_uri':callback_url,'client_id':client_id,'client_secret':client_secret}

    response = requests.post(auth_url,data=params)
    print response.status_code
    if response.status_code == 200:
        content = json.loads(response.text)
        token = content.get('access_token')
        session['access_token'] = token

        profile_url = 'https://api.linkedin.com/v1/people/~:(id,first-name,last-name)?oauth2_access_token='+token+'&format=json'
        response = requests.get(profile_url)
        if response.status_code == 200:
            data = json.loads(response.text)
            id = data.get('id')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            session['first_name'] = first_name
            session['last_name'] = last_name
            return redirect(SETTINGS['URL_BASE']+first_name+'.'+last_name)
    else:
        return render_template('error.html')

@app.route('/login',methods=['GET','POST'])
def login():
    print 'On Dev ? %s'%SETTINGS['ON_DEV']
    redirect_= request.args.get('redirect')
    if redirect_:
        session['redirect'] = redirect_
    callback_url = SETTINGS['URL_BASE']+'callback'
    code = str(uuid4()).replace('-','')
    print code
    # url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id='+SETTINGS['LINKEDIN_CLIENT_ID']+'&redirect_uri='+callback_url+'&state='+code+'&scope=r_fullprofile%20r_emailaddress%20w_share'
    url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id='+SETTINGS['LINKEDIN_CLIENT_ID']+'&redirect_uri='+callback_url+'&state='+code+'&scope=r_basicprofile%20r_emailaddress%20w_share'
    return redirect(url,code=302)

@app.route('/logout',methods=['GET','POST'])
def logout():
    del session['access_token']
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    session.pop('last_name', None)
    session.pop('first_name', None)
    session.pop('access_token', None)
    import time
    time.sleep(5)
    session.clear()
    session["__invalidate__"] = True
    # print session.get('last_name')
    # return redirect('/')
    return redirect('/'+first_name+'.'+last_name)

@app.after_request
def remove_if_invalid(response):
    if "__invalidate__" in session:
        response.delete_cookie(app.session_cookie_name)
    return response

@app.route('/<first_name>.<last_name>')
def resume(first_name,last_name):
    positions = []
    educations = []
    certifications = []
    css = None
    htmlcontent = None
    theme = Themes.query.filter_by(first_name=first_name).filter_by(last_name=last_name).first()
    if theme:
        htmlcontent = theme.html_content
        css = theme.css_content
    user = UserProfile.query.filter_by(first_name=first_name).filter_by(last_name=last_name).first()
    if user:
        positions = Positions.query.filter_by(user_id=user.user_id).all()
        educations = Education.query.filter_by(user_id=user.user_id).all()
        certifications = Certifications.query.filter_by(user_id=user.user_id).all()
    if htmlcontent :
        content = render_template_string(htmlcontent,first_name=first_name,last_name=last_name,
                                       user=user,positions=positions,educations=educations,
                                        certifications=certifications)
        print 'Saved content'
    else:
        content = render_template('basictheme.html',
                                   user=user,positions=positions,educations=educations,
                                    certifications=certifications)
    print 'Modified CSS %s'%css
    return render_template('resume.html',theme=content,themestyle=css,first_name=first_name,last_name=last_name)

@app.route('/edit/<first_name>.<last_name>')
def edit(first_name,last_name):
    positions = []
    educations = []
    certifications = []
    htmlcontent = None
    css = None
    theme = Themes.query.filter_by(first_name=first_name).filter_by(last_name=last_name).first()
    if theme:
        htmlcontent = theme.html_content
        css = theme.css_content
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if htmlcontent:
        content = htmlcontent
    else:
        filepath = os.path.join(dir_path,'templates','basictheme.html')
        f = open(filepath)
        content = f.read()
        f.close()

    return render_template('theme_editor.html',content=content,css=css,first_name=first_name,last_name=last_name)

@app.route('/save/<first_name>.<last_name>',methods=['POST'])
def save(first_name,last_name):
    html_content = request.form.get('html_content')
    css_content = request.form.get('css_content')
    # print 'HTML %s'%html_content
    print 'CSS %s'%css_content
    theme = Themes.query.filter_by(first_name=first_name).filter_by(last_name=last_name).first()
    # soup = BeautifulSoup(html_content)
    # html_content = soup.prettify(formatter=None)

    # soup = BeautifulSoup(css_content)
    # css_content = soup.prettify(formatter=None)
    if theme:
        theme.html_content = html_content
        theme.css_content = css_content
    else:
        theme = Themes(first_name=first_name,last_name=last_name,html_content=html_content,css_content=css_content)
        db.session.add(theme)

    db.session.commit()
    import time
    time.sleep(5)
    return redirect('/%s.%s'%(first_name,last_name))
@app.route('/')
def hello():
    print session.get('first_name')
    print session.get('last_name')
    print session.get('access_token')

    if session.get('access_token'):
        return render_template('home.html',access_token = session.get('acess_token'))
    else:
        return render_template('index.html')



if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0',debug=True)

