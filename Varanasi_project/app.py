from flask import Flask , render_template, request, redirect, flash,session,  url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from werkzeug.utils import redirect, secure_filename

app=Flask(__name__)
app.secret_key='Abcd1234'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///vnsdatabase.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS']=False

db=SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
   # __tablename__='user'
    user_id=db.Column(db.Integer,autoincrement=True, primary_key=True)
    username=db.Column(db.String(20),unique=True, nullable=False)
    email=db.Column(db.String(30),nullable=True)
    name=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(20),nullable=False)
    age=db.Column(db.Integer)
    blogs=db.relationship('Blog')

    ''' def __init__(self,username):
        self.username=username'''

class Blog(db.Model):
   # __tablename__='blog' 
    id=db.Column(db.Integer, primary_key=True)   
    message=db.Column(db.String(1000), nullable=False)
    #file=db.Column(db.LargeBinary, nullable=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))

    '''def __init__(self,message):
        self.message=message'''

    
@app.route('/')
def home():
    return render_template('Dashboard_.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if request.method=='GET':
        return render_template('dashboard.html') 

@app.route('/explore')
def explore():
    return render_template('explore.html') 

@app.route('/BHU')
def BHU():
    return render_template('BHU.html')    

@app.route('/ghats')
def ghats():
    return render_template('ghats.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html') 

@app.route('/review')
def review():
    userr=User.query.all()
    msg=Blog.query.all()
    return render_template('review.html', userr=userr, msg=msg)      
    
     # For register login logout

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        name=request.form['name']
        password=request.form['password']
        email=request.form['email'] 
        age=request.form['age'] 
        encpassword=sha256_crypt.encrypt(password)
        entry=User(username=username, name =name,email=email, password=encpassword, age=age)
        db.session.add(entry)
        db.session.commit()
        flash('Registered successfully')
        return redirect(url_for('login'))
 
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login(): 
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        pas=user.password
        if(sha256_crypt.verify(password,pas)):
            session['username']=username
            return render_template('dashboard.html',username=username)

        else:
            flash('invalid username/password')
            return redirect(url_for('login'))
     
    return render_template('login.html')        
         

@app.route('/logout')
def logout():
    session.pop('username',None)
    flash('Logged out successfully')
    return render_template('login.html')             

@app.route("/review_input", methods=["GET","POST"])
def review_input():
    if request.method=='POST':
        message=request.form['message']
        #  file=request.form['file']
        #  print(session)
        user=User.query.filter_by(username=session["username"]).first()
        data=Blog( message=message,user_id=user.user_id)
        db.session.add(data)
        db.session.commit()
        flash('You have posted successfully...')
        return render_template('review_input.html')

    return render_template('review_input.html')

@app.route('/card')
def card():
    return render_template('card.html')

@app.route('/reach_air')
def reach_air():
    return render_template('reach_air.html')

@app.route('/reach_road')
def reach_road():
    return render_template('reach_road.html')

@app.route('/read_rail')
def read_rail():
    return render_template('read_rail.html')            

'''  
@app.route("/update/<int:sno>")
def update(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    
@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")'''


if __name__ =="__main__":
    app.run(debug=True)            