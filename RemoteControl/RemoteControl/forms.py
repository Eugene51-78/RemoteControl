# -*- coding: utf-8 -*-
from django import forms
from splitjson.widgets import SplitJSONWidget

class testForm(forms.Form):
    attrs = {'email': 'special', 'size': '40'}
    data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))