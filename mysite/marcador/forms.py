from django import forms

from .models import Bookmark

class BookmarkForm(forms.ModelForm):
	class Meta:
		model = Bookmark
		exclude = ('date_created', 'date_updated', 'owner')
