import hashlib

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import JSONField, ManyToManyField
from django.utils import timezone

from .user import AppUser
from .base import DefaultToStringMixin, MainModel

# from ..validators import FileSizeValidator

UserModel = AppUser()

gender = (("female", "Female"),
          ("male", "Male"),
          ("diverse", "Diverse"),
          ("unknown", "Unknown"))


#
#
# class AppUserManager(BaseUserManager):
#     """
#     Custom user model manager where email is the unique identifiers
#     for authentication instead of usernames.
#     """
#
#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a user with the given email and password.
#         """
#         if not email:
#             raise ValueError("The Email must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("is_active", True)
#
#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")
#         return self.create_user(email, password, **extra_fields)
#
#
# class Employee(AbstractUser):
#     user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
#     email = models.EmailField(
#         "email address",
#         null=False,
#         blank=False,
#         unique=True,
#     )
#
#     is_staff = models.BooleanField(
#         default=False,
#     )
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     objects = AppUserManager()
#

class ClientCategory(DefaultToStringMixin, models.Model):
    denotation = models.CharField(max_length=4096)
    description = models.CharField(max_length=65536, null=True, blank=True)

    class Meta:
        ordering = ["denotation"]


class Client(models.Model):
    client_number = models.CharField(max_length=64, unique=True)
    date_creation = models.DateTimeField(null=True, blank=True)
    denotation = models.CharField(max_length=1024)
    description = models.CharField(max_length=65536, null=True, blank=True)
    client_category = models.ForeignKey(ClientCategory, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(null=True, default=timezone.now)

    def __str__(self):
        return str(self.client_number) + " " + str(self.denotation)


class ContactPerson(models.Model):
    gender = models.CharField(max_length=9, choices=gender)
    title = models.CharField(max_length=512, null=True, blank=True)
    institution_free = models.CharField(max_length=512, null=True, blank=True)
    institution_client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=True, blank=True)
    last_name = models.CharField(max_length=512)
    first_name = models.CharField(max_length=512, null=True, blank=True)
    division = models.CharField(max_length=512, null=True, blank=True)
    role = models.CharField(max_length=512, null=True, blank=True)
    comments = models.CharField(max_length=65536, null=True, blank=True)

    user = models.OneToOneField(UserModel, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.institution_client} - {self.user}"


class CrimeCategory(DefaultToStringMixin, models.Model):
    denotation = models.CharField(max_length=4096)
    description = models.CharField(max_length=65536, null=True, blank=True)

    class Meta:
        ordering = ["denotation"]


class Mandate(MainModel):
    mandate_number = models.CharField(max_length=64, unique=True)
    denotation = models.CharField(max_length=4096, null=True, blank=True)
    date_mandate_received = models.DateTimeField(default=timezone.now)
    details = JSONField(blank=True, default=dict)

    description = models.CharField(max_length=65536, null=True, blank=True)
    comments = models.CharField(max_length=65536, null=True, blank=True)
    priority = models.CharField(max_length=4096, default="")
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=True, blank=True)
    client_contact = models.ForeignKey(ContactPerson, on_delete=models.DO_NOTHING, null=True, blank=True)
    investigation_group = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=True, blank=True,
                                            related_name="investigation_group_set")
    investigation_group_contact = models.ForeignKey(ContactPerson, on_delete=models.DO_NOTHING, null=True, blank=True,
                                                    related_name="investigation_group_contact_set")

    # forensic_expert = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, blank=True)
    #
    # actual_report = models.ForeignKey("Report", on_delete=models.SET_NULL, null=True, blank=True,
    #                                   related_name="actual_report_reverse")
    #
    # related_files = ManyToManyField("AuditedFile", related_name='mandate_related_files', blank=True)
    # state_mandate = models.CharField(max_length=30, default="PRE_ORDER_ACCEPTED")
    # access = ManyToManyField(Employee, related_name='mandate_access_users', blank=True)
    def __str__(self):
        return f"{self.mandate_number} - {self.denotation}"


class MandateRelatedMixin(models.Model):
    mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE)

    class Meta:
        abstract = True
#
#
# class Report(models.Model):
#     mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE, related_name='reports')
#     file_number = models.CharField(max_length=4096, null=True, blank=True)
#     investigation_number = models.CharField(max_length=4096, null=True, blank=True)
#     crime_categories = ManyToManyField(CrimeCategory, blank=False)
#     date_internal_deadline = models.DateTimeField(null=True, blank=True)
#     date_external_deadline = models.DateTimeField(null=True, blank=True)
#     date_delivery = models.DateTimeField(null=True, blank=True)
#     report_number = models.CharField(max_length=4096, null=True, blank=True)
#     details = JSONField(blank=True, default=dict)
#
#
# class Task(MainModel):
#     denotation = models.CharField(max_length=4096)
#     description = models.CharField(max_length=65536, null=True, blank=True)
#     type = models.CharField(max_length=512)
#     priority = models.IntegerField(default=65536)
#     details = JSONField(blank=True, default=dict)
#     results = JSONField(blank=True, default=dict)
#     state_task = models.CharField(max_length=30)
#     reports = ManyToManyField(Report, related_name='tasks', blank=False)
#
#     @property
#     def report_text(self):
#         res = ""
#         res += (self.details.get("report_point")) or self.description or ""
#         res += "\n".join((i.get("report_point") or "") for i in self.details.get("sub_points", []))
#         return res.strip()
#
#
# class AuditedFile(models.Model, MandateRelatedMixin):
#     """ An audited file object. Keep in mind that uploading huge files balloons the database."""
#     description = models.CharField(max_length=4096, blank=True, null=True)
#     name = models.CharField(max_length=4096)
#     mime_type = models.CharField(max_length=128)
#     hash_sum = models.CharField(max_length=512)
#     size = models.BigIntegerField()
#     creator = models.ForeignKey(ContactPerson, on_delete=models.DO_NOTHING)
#
#     class Meta:
#         abstract = True
#
#     def __str__(self):
#         return self.name + " (%s)" % str(self.mime_type)
#
#     def update_data(self, data):
#         data = bytes(data)
#         hasher = hashlib.sha3_512()
#         hasher.update(data)
#         self.data = data
#         self.size = len(data)
#         self.hash_sum = hasher.hexdigest().lower()
#
#     def save(self, *args, **kwargs):
#         return super().save(*args, **kwargs)
#
#
# class WorkedTimeMandate(models.Model):
#     mandate = models.ForeignKey(Mandate, on_delete=models.DO_NOTHING)
#     id = models.BigIntegerField(primary_key=True)
#     main_task = models.CharField(max_length=65536, null=True, blank=True)
#     worked_time = models.DurationField()
#
#
# class UploadedFile(models.Model):
#     FILE_UPLOAD_DIRECTORY = 'uploaded_files/'
#     ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx', 'txt', 'mp4', 'avi', 'mov', 'jpg', 'jpeg', 'png', 'gif']
#     FILE_MAX_SIZE = 100 * 1024 * 1024  # 100 MB
#
#     file = models.FileField(
#         upload_to=FILE_UPLOAD_DIRECTORY,
#         validators=[
#             FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS),
#             FileSizeValidator(max_size=FILE_MAX_SIZE)
#         ]
#     )
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     uploaded_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.file.name
