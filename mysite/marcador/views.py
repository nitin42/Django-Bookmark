from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator



from .models import Bookmark
from .forms import BookmarkForm

def bookmark_list(request):
	bookmark_list = Bookmark.public.all()
	paginator = Paginator(bookmark_list, 4)

	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1

	try:
		bookmarks = paginator.page(page)
	except(EmptyPage, InvalidPage):
		bookmarks = paginator.page(paginator.num_pages)

	if request.GET.get('tag'):
		bookmark_list = bookmark_list.filter(tags__name=request.GET['tag'])

	context = {
		'bookmarks': bookmarks
	}
	return render(request, 'marcadar/bookmark_list.html', context)

# Allows to view each user's bookmarks
def bookmark_user(request, username):
	user = get_object_or_404(User, username=username) # Get the user from the DB
	if request.user == user:  # User authenticated
		bookmarks = user.bookmarks.all() # Show all the bookmarks of user
	else:
		bookmarks = Bookmark.public.filter(owner__username=username) # Else display the bookmarks by theri name on home

	if request.GET.get('tag'):
		bookmarks = bookmarks.filter(tags__name=request.GET['tag'])

	context = {
		'bookmarks': bookmarks, 'owner': user
	}
	return render(request, 'marcadar/bookmark_user.html', context)

@login_required
def bookmark_create(request):
	form = BookmarkForm(data=request.POST)
	if form.is_valid():
		bookmark = form.save(commit=False)
		bookmark.owner = request.user
		bookmark.save()
		form.save_m2m() # Save the many-to-many data (relationship to Tag model)
		return redirect('marcador_bookmark_user', username=request.user.username)
	else:
		form = BookmarkForm()

	context = {'form': form, 'create': True}
	return render(request, 'marcadar/form.html', context)

@login_required
def bookmark_edit(request, pk):
	bookmark = get_object_or_404(Bookmark, pk=pk) # Get the bookmark from the database
	if bookmark.owner != request.user and not request.user.is_superuser: # Check the authentication
		raise PermissionDenied
	if request.method == 'POST':
		form = BookmarkForm(instance=bookmark, data=request.POST) # Get the form with prefilled data.
		if form.is_valid():
			form.save()
			return redirect('marcador_bookmark_user', username=request.user.username)
	else:
		form = BookmarkForm(instance=bookmark)
	context = {'form': form, 'create': False}
	return render(request, 'marcadar/form.html', context)


