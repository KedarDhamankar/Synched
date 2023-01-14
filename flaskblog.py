from flask import Flask, render_template , url_for, flash, redirect
from forms import  *

app = Flask(__name__)

app.config['SECRET_KEY']='bc3f2d4569b0e21ce580e96cd8c8617c'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
    
@app.route("/commreg", methods=['GET','POST'])
def commreg():
    form=CommRegistration()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('commdash'))
    return render_template('commreg.html', title='Committee Register', form=form)
    
 
@app.route("/commlogin", methods=['GET','POST'])
def commlogin():
    form = CommLogin()
    if form.validate_on_submit():
            flash(f'Account logged for {form.username.data}!', 'success')
            return redirect(url_for('commdash'))
    return render_template('commlogin.html', title='Login', form=form)

@app.route("/adminlog", methods=['GET','POST'])
def adminlog():
    form = AdminLogin()
    if form.validate_on_submit():
            flash(f'Account logged in  for {form.username.data}!', 'success')
            return redirect(url_for('admindash'))
    return render_template('adminlog.html', title='Login', form=form)

@app.route("/adminreg", methods=['GET','POST'])
def adminreg():
    form=AdminRegistration()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('admindash'))
    return render_template('adminreg.html', title='Admin Register', form=form)

if __name__ =='__main__':
    app.run(debug=True)