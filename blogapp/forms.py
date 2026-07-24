from blogapp.models import Blogs
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Add_Blog_Form(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = "__all__"
        exclude = ["user","liked_by"]

class Edit_Blog_Form(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = "__all__"
        exclude = ["user","liked_by"]

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        self.fields["username"].widget.attrs.update({
            "placeholder": "Enter username"
        })

        self.fields["email"].widget.attrs.update({
            "placeholder": "Enter email"
        })

        self.fields["password1"].widget.attrs.update({
            "placeholder": "Enter password"
        })

        self.fields["password2"].widget.attrs.update({
            "placeholder": "Confirm password"
        })




