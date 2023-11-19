# from django import forms
# from django.forms import ModelForm
# from bankapp.models import Application, Branches
#
#
# class ApplicationForm(ModelForm):
#     class Meta:
#         model = Application
#         fields = "__all__"
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['branches'].queryset = Branches.objects.none()
