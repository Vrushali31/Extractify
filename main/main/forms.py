from django import forms

class UploadFileForm(forms.Form):
    filename = forms.FileField()
    filetype = forms.TextInput()
