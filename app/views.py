from flask import render_template, flash, request
from app import app
from flask import request
from wtforms import Form, validators, TextField, SelectField
from wtforms.fields.html5 import DateField
from wtforms_components import DateIntervalField, DateRange
from app import getdata
import json
from datetime import datetime
from flask_admin.form.widgets import DatePickerWidget




class ReusableForm(Form):
    name = TextField(default='username', validators=[validators.required()])
    lang = SelectField('Language', choices=[('en', 'English'), ('it', 'Italian'), ('de', 'Deutsch'), ('nl','Nederlands')], validators=[validators.required()])
    date = TextField('Start', default='Select date', validators=[validators.required()])



@app.route('/', methods=['GET', 'POST'])
@app.route('/index')


def index():

    form = ReusableForm(request.form)

    print form.errors
    data = None
    if request.method == 'POST':

        if form.validate():

            start, end = request.form['date'].split("-")

            name = request.form['name']

            lang = request.form['lang']

            s = start.replace("/", "")
            e = end.replace("/", "")

            startDate = s[-5:-1]+s[:2]+s[2:4]
            endDate = e[-4:]+e[1:3]+e[3:5]
            
            flash(name)

            data = getdata.launchQuery(name, lang, startDate, endDate)

            if not data:
                flash("No data, retry")



        else:

            flash('All the form fields are required. ')

    return render_template('index.html', form=form, data=data)



