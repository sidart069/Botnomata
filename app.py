from flask import Flask,render_template,url_for,request
from flask_material import Material
from datetime import datetime
from flask import Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,url_for, flash, redirect
from SEProject.forms import RegistrationForm, LoginForm
from flask_material import Material


app = Flask(__name__)
Material(app)

app.config['SECRET_KEY']='a857f8519efef4804da35c967de0e430'
#to protect the application from cross site cookies , fraud attacks
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)



# EDA PKg
import pandas as pd
import numpy as np

# ML Pkg
from sklearn.externals import joblib


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/preview')
def preview():
    df = pd.read_csv("data/iris.csv")
    return render_template("preview.html",df_view = df)




@app.route('/',methods=["POST"])
def analyze():
	if request.method == 'POST':
		petal_length = request.form['petal_length']
		sepal_length = request.form['sepal_length']
		petal_width = request.form['petal_width']
		sepal_width = request.form['sepal_width']
		model_choice = request.form['model_choice']

		# Clean the data by convert from unicode to float
		sample_data = [sepal_length,sepal_width,petal_length,petal_width]
		clean_data = [float(i) for i in sample_data]

		# Reshape the Data as a Sample not Individual Features
		ex1 = np.array(clean_data).reshape(1,-1)

		# ex1 = np.array([6.2,3.4,5.4,2.3]).reshape(1,-1)

		# Reloading the Model
		if model_choice == 'logitmodel':
		    logit_model = joblib.load('data/logit_model_iris.pkl')
		    result_prediction = logit_model.predict(ex1)
		elif model_choice == 'knnmodel':
		    knn_model = joblib.load('data/knn_model.sav')
		    result_prediction = knn_model.predict(ex1)
		'''elif model_choice == 'svmmodel':
			knn_model = joblib.load('data/svm_model_iris.pkl')
			result_prediction = knn_model.predict(ex1)'''

	return render_template('index.html', petal_width=petal_width,
		sepal_width=sepal_width,
		sepal_length=sepal_length,
		petal_length=petal_length,
		clean_data=clean_data,
		result_prediction=result_prediction,
		model_selected=model_choice)



@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account successfully created for{form.username.data}!','success' ) #success is from bootstrap
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form= form)



#LOGIN IS NOT COMPLETED ,NOT WORKING
@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@irisKIIT.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)
