from django import forms


class GitHubRepoSearchForm(forms.Form):
    username = forms.CharField(label='GitHub Username', max_length=100)
    language = forms.CharField(label='Preferred Language', max_length=50)
