from flask import render_template, flash, request
from app import app
from flask import request
from wtforms import Form, validators, TextField
from wtforms.fields.html5 import DateField
from wtforms_components import DateIntervalField, DateRange


from app import getdata
import json
from datetime import datetime
from flask_admin.form.widgets import DatePickerWidget


class ReusableForm(Form):
    name = TextField(default='username', validators=[validators.required()])
    start = TextField('Start', default='dd-mm-yyyy', validators=[validators.required()])
    end = TextField('End', default='dd-mm-yyyy', validators=[validators.required()])


@app.route('/', methods=['GET', 'POST'])
@app.route('/index')



def index():

    form = ReusableForm(request.form)

    print form.errors
    data = None
    if request.method == 'POST':

        if form.validate():

            name = request.form['name']

            # s = form.start.data.replace("-", "")
            # e = form.end.data.replace("-", "")

            s = request.form["start"].replace("-", "")
            e = request.form["end"].replace("-", "")


            startDate = s[-4:]+s[2:4]+s[:2]
            endDate = e[-4:]+e[2:4]+e[:2]

            flash(name)

            data = getdata.launchQuery(name, startDate, endDate)

            if not data:
                flash("No data, retry")


        else:

            flash('All the form fields are required. ')

    return render_template('index.html', form=form, data=data)



