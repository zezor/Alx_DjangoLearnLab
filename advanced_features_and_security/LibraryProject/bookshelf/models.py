from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()

    class Meta:
        permissions = (
            ("can_view", "Can view Book"),
            ("can_create", "Can create Book"),
            ("can_edit", "Can edit Book"),
            ("can_delete", "Can delete Book"),
        )

    def __str__(self):
         return f"{self.title} by {self.author} ({self.publication_year})"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("User must have an email")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(unique=True)
    profile_photo = models.ImageField(unique=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects  =UserManager()
