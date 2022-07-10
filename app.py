from flask import Flask,redirect,url_for,render_template,request,flash,Markup,session
from database import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.secret_key="srtyjhnbvgh"
#app.config["SQLALCHEMY_DATABASE_URI"]="postgres://uorwvfsjpyjtcn:df963883a654a2e4dd7d9cc59213ed56f76aa24fe34d8bc42907a03e673f08bb@ec2-44-199-143-43.compute-1.amazonaws.com:5432/d1bh8aq9q5gcbs"
logged=False
CurrentEarnigs = 0
CurrentCommision = 0
CurrentSales=0

@app.route('/')
def home():
    return render_template("Home.html")

@app.route("/login")
def login():
    if 'userName' not in session:
        return render_template('login.html')
    return redirect('/user')

@app.route("/user")
def user():
    if 'userName' in session:
        return render_template("User.html",products=getProductsDB())
    return redirect('/login')

@app.route('/authenticateUser',methods=['POST','GET'])
def authenticateUser():
    if request.method=='POST':
        if authenticate(request.form['userName'], request.form["password"]):
            session['userName'] = request.form['userName']
            return redirect('/user')
        flash(Markup("<div class='alert alert-danger' role='alert'>Invalid username/password</div>"))
        #flash(Markup('<div class="alert alert-danger alert-dismissible fade show" role="alert">Invalid username/password <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'))
    return redirect('/login')

@app.route("/update",methods=['POST','GET'])
def update():
    global CurrentEarnigs
    global CurrentCommision
    global CurrentSales
    global currenttime
    if 'userName' in session:
        if request.method == "POST":
            UpdateDB(generateQuantity(request.form.getlist("quantity[]")))
            commission=Commision(request.form['employeeID'],request.form.getlist("quantity[]"))
            CurrentCommision+=commission
            CurrentSales+=UpdateEmployee(request.form['employeeID'], request.form.getlist("quantity[]"), commission)
            CurrentEarnigs+=Earnings(request.form.getlist("quantity[]"))
            #Incase the number of products is more than 25 change the pagelength in the User.html js script
        return redirect("/user")
    return redirect('/login')

@app.route("/adminLogin")
def adminLogin():
    if 'AdminuserName' not in session:
        return render_template('Admin Login.html')
    return redirect('/admin')

@app.route("/admin")
def admin():
    #Make sure the form of Admin Login has the name=UserName
    if 'AdminuserName' in session:
        return render_template("Admin.html", currentE=CurrentEarnigs,currentC=CurrentCommision,currentS=CurrentSales)
    return redirect('/adminLogin')

@app.route('/authenticateAdmin',methods=['POST','GET'])
def authenticateadmin():
    if request.method=='POST':
        if authenticateAdminDB(request.form['UserName'], request.form["password"]):
            session['AdminuserName'] = request.form['UserName']
            return redirect('/admin')
        flash(Markup("<div class='alert alert-danger' role='alert'>Invalid username/password</div>"))
        #flash(Markup('<div class="alert alert-danger alert-dismissible fade show" role="alert">Invalid username/password <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'))
    return redirect('/adminLogin')

@app.route('/table')
def table():
    if 'AdminuserName' in session:
        return render_template("tables.html",products=getProductsDB())
    return redirect('/adminLogin')

@app.route('/chart')
def chart():
    if 'AdminuserName' in session:
        return render_template("charts.html",product=getEmployeesDB())
    return redirect('/adminLogin')

@app.route('/registeradmin')
def registerAdminDisplay():
    return render_template('Admin Register.html')

@app.route('/registeradminDB',methods=['POST','GET'])
def registerAdminDB():
    if request.method=='POST':
        addAdmin(request.form)
        flash(Markup("<div class='alert alert-success' role='alert'>Account Created</div>"))
    return redirect('/registeradmin')

@app.route('/logout')
def logout():
    global CurrentEarnigs
    global CurrentCommision
    global CurrentSales
    session.pop('userName',None)
    session.pop('AdminuserName', None)
    inTialiseEmployees()
    CurrentSales=0
    CurrentCommision=0
    CurrentEarnigs=0
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

