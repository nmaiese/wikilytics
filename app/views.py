from flask import render_template, flash, request
from app import app
from flask import request
from wtforms import Form, validators, TextField, SelectField
from wtforms.fields.html5 import DateField
from wtforms_components import DateIntervalField, DateRange
from app import getdata
import json
import datetime
from flask_admin.form.widgets import DatePickerWidget




class ReusableForm(Form):
    name = TextField(default='username', validators=[validators.required()])
    date = TextField('Start', default='Select date', validators=[validators.required()])



@app.route('/', methods=['GET', 'POST'])
@app.route('/index')


def index():


    form = ReusableForm(request.form)

    print form.errors
    data = None
    name = None
    if request.method == 'POST':

        if form.validate():

            start, end = request.form['date'].split("-")

            name = request.form['name']

            s = start.replace("/", "")
            e = end.replace("/", "")

            startDate = s[-5:-1]+s[:2]+s[2:4]
            endDate = e[-4:]+e[1:3]+e[3:5]
            
            flash(name)

            data, errors = getdata.launchQuery(name, startDate, endDate)

            if not data:
                flash("No data, retry")
                flash(errors)



        else:

            flash('All the form fields are required. ')

    return render_template('index.html', form=form, data=data, query=name)




@app.route('/trends')

def trends():

    form = ReusableForm(request.form)


    supported_languages = ['en','it','de','nl','sv','ceb','de','fr','ru','es']
    lang = request.accept_languages.best_match(supported_languages)

    data = getdata.getTrends(lang=lang)
    query_list = ''

    for d in data[0]: 
        if d['rank'] < 11:
            if (d['article'] != 'Pagina_Principale' and d['article'] != 'Pagina_Principale'):
                flash(d['article'])
                query_list += ((d['article'])+',')

    query_list = query_list[:-1]
    form.name = query_list
    
    end = datetime.datetime.today() 
    start = end - datetime.timedelta(days=60)

    startDate = str('%02d' % start.year)+str('%02d' % start.month)+str('%02d' % start.day)
    endDate =  str('%02d' % end.year)+str('%02d' % end.month)+str('%02d' % end.day)
    
    flash(query_list)

    data, errors = getdata.launchQuery(query_list, startDate, endDate)
    if not data:
        flash("No data, retry")
        flash(errors)


    return render_template('index.html',form=form, data=data, query=query_list)






