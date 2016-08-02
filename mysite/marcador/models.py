from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now

class Tag(models.Model):
	name = models.CharField(max_length=250, unique=True) # Name of the tag should be unique

	class Meta:
		verbose_name = 'tag'
		verbose_name_plural = 'tags'
		ordering = ['name']

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name


class PublicBookmarkManager(models.Manager):
	def get_queryset(self):
		qs = super(PublicBookmarkManager, self).get_queryset()
		return qs.filter(is_public=True)


class Bookmark(models.Model):
	url = models.URLField()
	title = models.CharField('title', max_length=250)
	description = models.TextField('description', blank=True)
	is_public = models.BooleanField('public', default=True)
	date_created = models.DateTimeField('date_created', default=timezone.now)
	date_updated = models.DateTimeField('date updated', default=timezone.now)
	owner = models.ForeignKey(User, verbose_name='owner', related_name='bookmarks')
	tags = models.ManyToManyField(Tag, blank=True) # Relation between tag and a bookmark
	objects = models.Manager()
	public = PublicBookmarkManager()

	class Meta:
		verbose_name = 'bookmark'
		verbose_name_plural = 'bookmarks'
		ordering = ['-date_created',] # Descending order of date 

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.id: # If the ID field is not present in the database then create it
			self.date_created = now()
		self.date_updated = now()
		super(Bookmark, self).save(*args, **kwargs)




