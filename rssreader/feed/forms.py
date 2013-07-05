#-*- coding: utf-8 -*-
from flask.ext.wtf import Form, TextField, Required, SubmitField


class SubscribeForm(Form):
    url = TextField("Url", validators=[Required()])
    submit = SubmitField("Subscribe")
