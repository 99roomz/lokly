import os
from flask import Flask, render_template, jsonify,request
from Address import parser
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import random
from flask_mail import Message

search_limit_guest = [10]
search_limit_user = [100]

if not os.path.exists('temp/database/'):
    os.makedirs('temp/database/')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp/database/user.db'
app.config['SQLALCHEMY_BINDS'] = { 'ip_database' :'sqlite:///temp/database/guest.db','address' :'sqlite:///temp/database/address.db'}
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.getenv('email', "indilokly@gmail.com"),
    MAIL_PASSWORD = os.getenv('password',"lokly1234"),
))
db = SQLAlchemy(app)
mail = Mail(app)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(40))
    company_name = db.Column(db.String(40))
    email = db.Column(db.String(40),unique = True)
    contact_number = db.Column(db.String(10),unique = True)
    password = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow())
    number_of_queries = db.Column(db.Integer,default=0)
    verified = db.Column(db.Integer,default = 0)
    otp = db.Column(db.Integer,default = -1)

    

    def __repr__(self):
        return '< Task %r >' % self.id

class Guests(db.Model):
    __bind_key__ = 'ip_database'
    id = db.Column(db.Integer,primary_key = True)
    ip =  db.Column(db.String(40))
    number_of_requests = db.Column(db.Integer,default=0)

    def __repr__(self):
        return '< Task %r >' % self.id

class AddressData(db.Model):
    __bind_key__ = 'address'
    id = db.Column(db.Integer,primary_key = True)
    address_input = db.Column(db.String(40))
    house_no = db.Column(db.String(40))
    street = db.Column(db.String(40))
    micro_locality = db.Column(db.String(40))
    sub_locality = db.Column(db.String(40))
    locality = db.Column(db.String(40))
    neighborhood = db.Column(db.String(40))
    city = db.Column(db.String(40))
    state = db.Column(db.String(40))
    country = db.Column(db.String(40))
    postal = db.Column(db.Integer)

    def __repr__(self):
        return '< Task %r >' % self.id

db.create_all()


@app.route('/')
def index():

    guest_ip_address = str(request.remote_addr)
    t_guest_user = Guests.query.filter_by(ip = guest_ip_address).first()
    if(t_guest_user==None):
        return render_template('Parser.html',already_used = 0)
    return render_template('Parser.html',already_used = t_guest_user.number_of_requests)


@app.route('/_get_data/', methods=['POST','GET'])
def _get_data():
    address=request.args.get('address')
    user_id = request.args.get('user_id')
    # print(address)
    # print(user_id)
    if (user_id!='Guest' and user_id!='null' and user_id!='' ):
        t_user = Users.query.get(int(user_id))
        if address=='':
            return jsonify({'data':'Please enter Address','queries':t_user.number_of_queries,'limit':search_limit_user[0]})
        if t_user.number_of_queries>=search_limit_user[0]:
            return jsonify({'data':'Search limit reached','queries':t_user.number_of_queries,'limit':search_limit_user[0]})
            
            
        parsed=parser(address)
        address_data = AddressData(address_input = address , house_no = parsed['House No'],street=parsed['Street'],micro_locality=parsed['Micro Locality'],sub_locality=parsed['Sublocality'],locality=parsed['Locality'],neighborhood=parsed['Neighbourhood'],city=parsed['City'],state=parsed['State'],country=parsed['Country'],postal=parsed['Postal'])
        db.session.add(address_data)
        db.session.commit()

        t_user.number_of_queries+=1
        db.session.commit()
        return jsonify({'Parsed_address': render_template('response.html', result=parsed),'queries':t_user.number_of_queries,'limit':search_limit_user[0]})
    else:
        guest_ip_address = str(request.remote_addr)
        t_guest_user = Guests.query.filter_by(ip = guest_ip_address).first()
        if address=='':
            return jsonify({'data':'Please enter Address','queries':t_guest_user.number_of_requests,'limit':search_limit_guest[0]})
        if(t_guest_user==None):
            t_guest_user = Guests(ip = guest_ip_address)
            db.session.add(t_guest_user)
            db.session.commit()
        t_guest_user = Guests.query.filter_by(ip = guest_ip_address).first()
        if t_guest_user.number_of_requests>=search_limit_guest[0]:
            return jsonify({'data':'Search limit reached. Sign Up for more searches','queries':t_guest_user.number_of_requests,'limit':search_limit_guest[0]})
            
        parsed = parser(address)
        address_data = AddressData(address_input = address , house_no = parsed['House No'],street=parsed['Street'],micro_locality=parsed['Micro Locality'],sub_locality=parsed['Sublocality'],locality=parsed['Locality'],neighborhood=parsed['Neighbourhood'],city=parsed['City'],state=parsed['State'],country=parsed['Country'],postal=parsed['Postal'])
        db.session.add(address_data)
        db.session.commit()

        t_guest_user.number_of_requests+=1
        db.session.commit()
        return jsonify({'Parsed_address': render_template('response.html', result=parsed),'queries':t_guest_user.number_of_requests,'limit':search_limit_guest[0]})

    
@app.route('/_logout/', methods=['POST','GET'])
def _logout():
    guest_ip_address = str(request.remote_addr)
    t_guest_user = Guests.query.filter_by(ip = guest_ip_address).first()
    if(t_guest_user==None):
        t_guest_user = Guests(ip = guest_ip_address)
        db.session.add(t_guest_user)
        db.session.commit()
    return jsonify({'queries':t_guest_user.number_of_requests,'limit':search_limit_guest[0]})
    
@app.route('/signup')
def signup():
    return render_template('signup.html')
    
@app.route('/loginpage')
def loginpage():
    return render_template('loginpage.html')    
    
@app.route('/about')
def about():
    return render_template('about.html')    
    
@app.route('/contact')
def contact_us():
    return render_template('contact.html')  
@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/send_otp',methods=['POST','GET'])
def send_otp():
    contactno = request.args.get('contact_no')
    password = request.args.get('password')
    name = request.args.get('name')
    company = request.args.get('company')
    email = request.args.get('email')
    domains = open("static/Invalid.txt","r")

    if (contactno=='' or password=='' or name=='' or company=='' or email==''):
        return jsonify({'data': 'Fill all fields'})

    for domain in domains:
        if domain.strip('\n') in email.split('@'):
            return jsonify({'data': 'Please enter corporate email_id'})

    t_user = Users.query.filter_by(contact_number = contactno).first()
    t_user1 = Users.query.filter_by(email = email).first()
    temp = random.randrange(1000,9999)
    if t_user1!=None:
        if t_user1.verified == 1:
            return jsonify({ 'data' :'Email id already exist'})
    if t_user!=None:
        if t_user.verified == 1:
            return jsonify({ 'data' :'Mobile No already exist'})

    

    if t_user!=None and t_user1!=None:
        if t_user1!=t_user:
            db.session.delete(t_user1)
    if t_user==None:
        t_user=t_user1
    if t_user==None:
        t_user = Users(contact_number = contactno , password = password ,name = name,email = email,company_name = company,number_of_queries=0,verified=0,otp=temp)
        db.session.add(t_user)
        db.session.commit()

    else:
        new_user = Users(contact_number = contactno , password = password ,name = name,email = email,company_name = company,verified=0,otp=temp)
        db.session.delete(t_user)
        t_user1 = Users.query.filter_by(contact_number = email).first()
        db.session.commit()
        db.session.add(new_user)
        db.session.commit()
        
    msg = Message("Verification Code for Indilokly",sender="hello@lokly.in",recipients=[email])
    msg.body = "Hello ,your verification code for indilokly is "+str(temp)
    try:
        mail.send(msg)
    except:
        return jsonify({"data":"Email id does not exist"})
    n_t_user = Users.query.filter_by(contact_number = contactno).first()
    n_t_user.otp = temp     
    db.session.commit()           
    return jsonify({'id':n_t_user.id})
    
@app.route('/submit_otp',methods=['POST','GET'])
def submit_otp():
    id = request.args.get('id')
    otp = request.args.get('otp')
    if (id=='' or otp==''):
        return jsonify({'data': 'Fill all fields'}) 
    try:
        otp = int(otp)
        if otp<1000 or otp>9999:
            return jsonify({'data': 'Invalid OTP'})
    except:
        return jsonify({'data': 'Invalid OTP'})
    t_user = Users.query.get(int(id))
    correct_otp=t_user.otp

    if int(otp)==int(correct_otp):
        t_user.verified=1
        db.session.commit()
        return jsonify({'id':t_user.id})
    else:
        return jsonify({'data':'Invalid OTP'})
    


@app.route('/send_otp_to_login',methods=['POST','GET'])
def send_otp_to_login():
    user_email = request.args.get('email_login')
    t_user = Users.query.filter_by(email = user_email).first()
    if(t_user==None):
        return jsonify({ 'data':'Not registered. Please create a account.'})
    if(t_user.verified == 0):
        return jsonify({'data':'Not verified. Please go to sign up page to verify.'})

    
    temp = random.randrange(1000,9999)
    t_user.otp = str(temp)
    db.session.commit()
    msg = Message("Verification Code for Indilokly",sender="hello@lokly.in",recipients=[user_email])
    msg.body = "Hello ,your verification code for indilokly is "+str(temp)
    try:
        mail.send(msg)
    except:
        return jsonify({"data":"Email id does not exist"})
    return jsonify({"id":t_user.id,"correct_otp":t_user.otp})

@app.route('/login_via_otp',methods = ['POST','GET'])
def log_via_otp():

    user_id = request.args.get('user_id')
    entered_otp = request.args.get('otp_login')
    correct_otp = Users.query.get(int(user_id)).otp
    c_user = Users.query.get(int(user_id))
    if int(entered_otp)!=int(correct_otp):
        return jsonify({'data': 'Incorrect Otp'})
    return jsonify({'id':c_user.id,'name': c_user.name,'queries':c_user.number_of_queries,'limit':search_limit_user[0]})

@app.route('/refresh',methods = ['POST','GET'])
def refresh():  
    user_id = request.args.get('user_id')
    c_user = Users.query.get(int(user_id))
    return jsonify({'name': c_user.name,'queries':c_user.number_of_queries,'limit':search_limit_user[0]})



if __name__ == "__main__":
    app.run(host = '0.0.0.0',debug=True,port=80)