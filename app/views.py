from flask import render_template, flash, request
from app import app
from flask import request
from wtforms import Form, validators, TextField, SelectField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms_components import DateIntervalField, DateRange
from app import getdata
import json
import datetime
from flask_admin.form.widgets import DatePickerWidget

class ReusableForm(Form):
    name = TextField(validators=[validators.required()])
    date = TextField('Start', default='Select date', validators=[validators.required()])
    languages = SelectMultipleField('Languages', choices=[('en', 'English'), ('it', 'Italian'), ('nl','Nederlands'), ('sv','Swedish'),('ceb','Cebuano'),('de','German'),('fr', 'French'),('ru', 'Russian'),('es','Spanish')], validators=[validators.required()])
    dataBtn = SubmitField(label='Get Data')


class TrendsForm(Form):
    languages = SelectField('Languages', choices=[('en', 'English'), ('it', 'Italian'), ('nl','Nederlands'), ('sv','Swedish'),('ceb','Cebuano'),('de','German'),('fr', 'French'),('ru', 'Russian'),('es','Spanish')], validators=[validators.required()])
    trendBtn = SubmitField(label='Get Last Trends')





@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():

    # supported_languages = ['en','it','de','nl','sv','ceb','fr','ru','es']
    # langs = []
    # langs.append(request.accept_languages.best_match(supported_languages))
    # if langs == [] or not langs or langs == [None]:
    #     langs = ['it']

    form = ReusableForm(request.form)
    trendForm = TrendsForm(request.form)

    name = 'All the form fields are required'
    data = []
    form_input = name

    #data, form_input, name = getdata.acquireTrends(langs)


    if trendForm.validate() and trendForm.trendBtn.data:
        if trendForm.validate():
            langs =  [trendForm.languages.data]
            data, form_input, name = getdata.acquireTrends(langs)
        else:
            name = 'All the form fields are required'
            data = []


    if form.validate() and form.dataBtn.data:

        if form.validate():
            start, end = request.form['date'].split("-")
            name = request.form['name']
            langs =  form.languages.data
            s = start.replace("/", "")
            e = end.replace("/", "")
            startDate = s[-5:-1]+s[:2]+s[2:4]
            endDate = e[-4:]+e[1:3]+e[3:5]
            form_input = name
            data, errors = getdata.launchQuery(name, startDate, endDate, langs)
        else:
            name = 'All the form fields are required'
            data = []

    return render_template('index.html', form=form, trendForm=trendForm, data=data, name=name.replace('_',' '), query=form_input)
