from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail

class UserManager(BaseUserManager, models.Manager):

	def _create_user(self, username, email, password, is_staff,
				is_superuser, **extra_fields):

		email = self.normalize_email(email)
		if not email:
			raise ValueError('El email debe ser obligatorio')
		user = self.model(username = username, email=email, is_active=True,
				is_staff = is_staff, is_superuser = is_superuser, **extra_fields)
		user.set_password(password)
		user.save( using = self._db)
		return user

	def create_user(self, username, email, password=None, **extra_fields):
		return self._create_user(username, email, password, False,
				False, **extra_fields)

	def create_superuser(self, username, email, password=None, **extra_fields):
		return self._create_user(username, email, password, True,
				True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

	username = models.CharField(unique=True, max_length=50)
	email = models.EmailField()
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	url_photo = models.URLField()
	has_permission = models.BooleanField(default=False)

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def get_short_name(self):
		return self.first_name

	def get_full_name(self):
		return '%s %s' % (self.first_name, self.last_name)

	def save(self, *args, **kw):
		if self.pk is not None:
			orig = User.objects.get(pk=self.pk)
			if orig.has_permission != self.has_permission and not orig.has_permission:
				send_mail(
					'Subject here',
					'Here is the message.',
					'sistemaosef@gmail.com',
					[orig.email],
					fail_silently=True,
				)		
		super(User, self).save(*args, **kw)
