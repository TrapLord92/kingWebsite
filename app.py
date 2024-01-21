from flask import Flask,redirect,url_for, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PhoneNumberType



import os
 

# DATABASE STUFF
project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(
    os.path.join(project_dir,"mydatabase.db")
)



app=Flask(__name__)
# configApp to DataBase
app.config["SQLALCHEMY_DATABASE_URI"]=database_file
db=SQLAlchemy(app)
app.app_context().push()







class User(db.Model):
  
    name = db.Column(db.String(100), nullable=False,primary_key=True,unique=False)
    phone = db.Column(PhoneNumberType(),nullable=False,unique=True)
   
  

    #TheORM
    


@app.route("/checkout",methods=['POST'])

def check_out():
    name=request.form['name']
    phone=request.form["phone"]
    # ConnectingTodataBase adding entry to the dataBase

    user=User(name=name,phone=phone)
    db.session.add(user)
    # commetingChangesToTheDB
    db.session.commit()

    # return 'Thank you for your order your contact info are: name %s and your phone is %s  ' %(name,phone)
   
    return render_template("checkout.html",name=name,phone=phone)

@app.route('/delete',methods=['POST'])
def delete():
    name=request.form['name']
    phone=User.query.filter_by(name=name).first()
    db.session.delete(phone)
    db.session.commit()
    return redirect('/clientOrdens')
    
    


@app.route('/')
# handling request
def index():
    return render_template("index.html")

@app.route('/admin/<name>')
def welcome_admin(name):

    if name =="KING": 
        return redirect(url_for('ordens'))
    else:
        return redirect(url_for('index'))

@app.route('/clientOrdens')
def ordens():
    ordens= User.query.all()
  
    return render_template('clienteInfo.html',ordens=ordens)


if __name__ == "__main__":
    app.run(debug=False)

