from django.db import models
from django.contrib.auth.models import PermissionsMixin,BaseUserManager,AbstractBaseUser
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
import random
import string

class UserManager(BaseUserManager):
    def create_user(self, email, name, qr_code=None, password=None):
        if not email:
            raise ValueError('User must have a valid email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, qr_code=qr_code)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin,AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    qr_code = models.ImageField(blank=True, upload_to='qr_code/')
    random_number = models.CharField(max_length=10, default='',blank=True,)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.name
    def __str__(self):
        return self.email
    
    def save(self,*args, **kwargs):
        if not self.qr_code:
            qrcode_img = qrcode.make(self.name)
            canvas = Image.new('RGB',(qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
            canvas.paste(qrcode_img)
            buffer = BytesIO()
            fname = f'qr_code_for_{self.name,self.email}.png'
            canvas.save(buffer,'PNG')
            self.qr_code.save(fname,ContentFile(buffer.getvalue()), save=False)

        if not self.random_number:
            # Generate a random 10-character string (mix of letters and digits)
            self.random_number = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        super().save(*args, **kwargs)
    

    