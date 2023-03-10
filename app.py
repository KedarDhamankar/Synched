from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

from sqlhelpers import *
from forms import *

import time

#initialize the app
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'SBP'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize mysql
mysql = MySQL(app)

#log in admin
def log_in_admin(username):
    users = Table("users", "name", "email", "username", "password")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

#log in committee
def log_in_committee(username):
    users = Table("users", "name", "email", "username", "password")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

#Registration page for admin
@app.route("/adminreg", methods = ['GET', 'POST'])
def adminreg():
    form = AdminRegistration(request.form)
    users = Table("username", "email", "password")

    #if form is submitted
    if request.method == 'POST':
        #collect form data
        username = form.username.data
        email = form.email.data

        #make sure user does not already exist
        if isnewuser(username):
            #add the user to mysql and log them in
            password = form.password.data
            cur = mysql.connection.cursor()
            cur.execute("insert into admin_details values('%s','%s','%s')" %(username,email,password))
            mysql.connection.commit()
            cur.close()
            log_in_admin(username)
            flash('User logged in', 'success')
            return redirect(url_for('admindash'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('adminreg'))

    return render_template('adminreg.html', form=form)

#Login page for Admin
@app.route("/adminlogin", methods = ['GET', 'POST'])
def adminlogin():
    #if form is submitted
    form = AdminRegistration(request.form)
    if request.method == 'POST':
        #collect form data
        email = request.form['email']
        candidate = request.form['password']

        #access users table to get the user's actual password
        users = Table("username", "email", "password")
        # user = users.getone("email", email)
        cur = mysql.connection.cursor()
        user = cur.execute("select * from admin_details where email = '%s'" %(email))
        print(user)
        if user > 0: 
            data = cur.fetchone()
        cur.close()
        accPass = data['password']
        username = data['username']

        #if the password cannot be found, the user does not exist
        if accPass is None:
            flash("Email is not found", 'danger')
            return redirect(url_for('adminlogin'))
        else:
            #verify that the password entered matches the actual password
            if candidate == accPass:
                #log in the user and redirect to Dashboard page
                log_in_committee(username)
                flash('You are now logged in.', 'success')
                return redirect(url_for('admindash'))
            else:
                #if the passwords do not match
                flash("Invalid password", 'danger')
                return redirect(url_for('adminlogin'))

    return render_template('adminlog.html', form=form)

#Registration page for committee
@app.route("/commreg", methods = ['GET', 'POST'])
def commreg():
    form = CommRegistration(request.form)
    users = Table("username", "id", "password")

    #if form is submitted
    if request.method == 'POST':
        #collect form data
        username = form.username.data
        id = form.id.data

        #make sure user does not already exist
        if isnewuser(username):
            #add the user to mysql and log them in
            password = form.password.data
            cur = mysql.connection.cursor()
            cur.execute("insert into comm_details values('%s','%s','%s')" %(username,id,password))
            mysql.connection.commit()
            cur.close()
            log_in_admin(username)
            return redirect(url_for('committeedash'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('committeedash'))

    return render_template('commreg.html', form=form)

#Login page for committee
@app.route("/committeelogin", methods = ['GET', 'POST'])
def committeelogin():
    #if form is submitted
    form = CommRegistration(request.form)
    if request.method == 'POST':
        #collect form data
        id = request.form['id']
        candidate = request.form['password']

        users = Table("username", "id", "password")
        # user = users.getone("email", email)
        cur = mysql.connection.cursor()
        user = cur.execute("select * from comm_details where id = '%s'" %(id))
        print(user)
        if user > 0: 
            data = cur.fetchone()
        cur.close()
        accPass = data['password']
        username = data['username']

        #if the password cannot be found, the user does not exist
        if accPass is None:
            flash("Email is not found", 'danger')
            return redirect(url_for('committeelogin'))
        else:
            #verify that the password entered matches the actual password
            if candidate == accPass:
                #log in the user and redirect to Dashboard page
                log_in_committee(username)
                flash('You are now logged in.', 'success')
                return redirect(url_for('committeedash'))
            else:
                #if the passwords do not match
                flash("Invalid password", 'danger')
                return redirect(url_for('committeelogin'))

    return render_template('commlogin.html', form=form)

#logout the user. Ends current session
@app.route("/logout")
def logout():
    session.clear()
    flash("Logout success", "success")
    return redirect(url_for('index'))

#Admin Dashboard page
@app.route("/admindash", methods = ['GET','POST'])
def admindash():
    csr=mysql.connection.cursor()
    resultValue=csr.execute("SELECT * FROM users where status=1")
    if resultValue>0:
        eventDetails= csr.fetchall()
        if request.method=='POST':
            response=request.form
            add = response['add']
            # print('hi')
            # print(add)
            if add != None:
                csr.execute("UPDATE users SET status=%s WHERE request_number=%s", (2,add))
            subtract=response['subtract']
            if subtract != None:
                csr.execute("UPDATE users SET status=%s WHERE request_number=%s", (0,subtract))
            mysql.connection.commit()
            csr.close()
        # return redirect(url_for('admindash'))
    return render_template('admindash.html', event_Details=eventDetails)
    
#Committee Dashboard page
@app.route("/committeedash", methods=['POST','GET'])
def committeedash():
    if request.method=='POST':
        details=request.form
        name=details['name']
        id=details['id']
        event=details['event']
        event_desc=details['event_desc']
        date=details['date']
        start=details['start']
        end=details['end']
        venue=details['venue']
        reqr=details['reqr']
        request_number=details['request_number']
        csr=mysql.connection.cursor()
        csr.execute("INSERT INTO users(name, id, event, event_desc, date, start, end, venue, reqr, request_number) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, id, event, event_desc, date, start, end, venue, reqr, request_number))
        mysql.connection.commit()
        csr.close()
        return redirect(url_for('committeedash'))
    return render_template('commdash.html')

#VJTI Map
@app.route("/map")
def vjti_map():
    return render_template('map.html')

#Index page
@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html')

@app.route('/timetable')
def calendar():
    crsr = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result= crsr.execute("SELECT event, start, end FROM users WHERE status = 2")
    if result>0:
        # event = crsr.fetchall()
        event=crsr.fetchone()
    crsr.close()
    print(event)
    name=event['event']
    date=event['date']
    # start= event['start']
    # end=event['end']
    # data={'Event':name, 'Date': date, 'Start': start, 'End':end}
    data={'Event':name, 'Date': date, 'End date': date}
    return render_template('calendar.html', events=data)

#Run app
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)