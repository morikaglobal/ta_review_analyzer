from wtforms import Form, StringField

class UrlSearchForm(Form):
    search = StringField('')