#!/usr/bin/env python
#-*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, Required, PasswordField, SubmitField

class LoginForm(Form):
    login = TextField("Login", validators=[Required()])
    password = PasswordField("Password", validators=[Required()])
    submit = SubmitField("Sign in")

