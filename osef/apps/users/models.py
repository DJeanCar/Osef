from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from apps.main.models import TimeStamp

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

	_TYPE = (
		('socio', 'Socio'),
		('almacen', 'Almancén'),
	)

	username = models.CharField(unique=True, max_length=50)
	email = models.EmailField()
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	url_photo = models.URLField(null=True, blank=True)
	photo = models.ImageField(upload_to = 'users', null=True, blank=True)
	has_permission = models.BooleanField(default=False)
	kind = models.CharField(max_length=15, choices=_TYPE, null=True, blank=True)

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return "%s | %s" % (self.username, self.kind)

	def get_short_name(self):
		return self.first_name

	def get_full_name(self):
		return '%s %s' % (self.first_name, self.last_name)

	def save(self, *args, **kw):
		if self.pk is not None:
			orig = User.objects.get(pk=self.pk)
			if orig.has_permission != self.has_permission and not orig.has_permission:
				html_content = 'El administrador te a dado permisos de acceso a Osef, puedes ingresar en <a href="http://localhost:8000">dominio.com</a>'
				msg = EmailMultiAlternatives(
					'Tu cuenta en Osef a sido activada',
					html_content,
					'Osef <mjeanc.104@gmail.com>',
					[orig.email],
				)
				msg.attach_alternative(html_content, 'text/html')
				# msg.send()
		super(User, self).save(*args, **kw)


class Account(models.Model):

	_TYPE = (
		('Dólares', 'Dólares'),
		('Pesos mexicanos', 'Pesos mexicanos'),
	)
	_CURRENCY = (
		('usd', 'USD'),
		('mxn', 'MXN'),
	)

	name = models.CharField(max_length=50, choices=_TYPE)
	currency = models.CharField(max_length=15, choices=_CURRENCY)
	amount = models.BigIntegerField()

	def __str__(self):
		return self.name


from apps.stores.models import Movement, SocioMovement
class Notification(TimeStamp):

	user = models.ForeignKey(User)
	sender = models.ForeignKey(User, related_name='sender')
	store_movement = models.ForeignKey(Movement, null=True, blank=True)
	socio_movement = models.ForeignKey(SocioMovement, null=True, blank=True)
	description = models.CharField(max_length=100)
	viewed = models.BooleanField(default=False)

	def __str__(self):
		return self.description

class Comment(TimeStamp):

	user = models.ForeignKey(User)
	notification = models.ForeignKey(Notification)
	content = models.CharField(max_length=100)

	def __str__(self):
		return self.content
