import uuid

from django.contrib import admin
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.utils.text import slugify
from datetime import datetime

from .utils import gravatar_url


class Base(models.Model):
    slug = models.SlugField(
        null=False,
        verbose_name="URL",
        help_text="A short label, generally used in URLs.",
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this object should be treated as active. Unselect this instead of deleting objects.",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-date_created"]


class CommonInfo(models.Model):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    SEX_CHOICES = {
        MALE: "Male",
        FEMALE: "Female",
        OTHER: "Other",
    }

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    phone = models.CharField(max_length=10, null=True, blank=True)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=OTHER,
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    """
    Represents a user available in system.
    """

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        STUDENT = "STUDENT", _("Student")
        INSTRUCTOR = "INSTRUCTOR", _("Instructor")

    base_role = Roles.ADMIN

    role = models.CharField(
        max_length=20, choices=Roles, default=base_role, help_text="Role of the user"
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/%d/",
        null=True,
        blank=True,
        help_text="Upload avatar of the user",
        storage=MediaCloudinaryStorage(),
    )
    reset_code = models.CharField(max_length=7, null=True, blank=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-date_joined"]

    @admin.display(description="Full Name")
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    @admin.display(description="Preview")
    def avatar_preview(self):
        if self.avatar:
            return mark_safe(
                f'<img src="{self.avatar.url}" alt="{self.username}" width="75" height="75" class="img-thumbnail rounded-circle shadow" />'
            )

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = gravatar_url(self.email)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class StudentManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Roles.STUDENT)


class StudentProxy(User):
    base_role = User.Roles.STUDENT

    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = "student"
        verbose_name_plural = "students"

    def save(self, *args, **kwargs):
        self.role = User.Roles.STUDENT
        return super().save(*args, **kwargs)


class Student(CommonInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class InstructorManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Roles.INSTRUCTOR)


class InstructorProxy(User):
    base_role = User.Roles.INSTRUCTOR

    objects = InstructorManager()

    class Meta:
        proxy = True
        verbose_name = "instructor"
        verbose_name_plural = "instructors"

    def save(self, *args, **kwargs):
        self.role = User.Roles.INSTRUCTOR
        return super().save(*args, **kwargs)


class Instructor(CommonInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Category(Base):
    """
    Represents a category available in system.
    """

    label = models.CharField(unique=True, max_length=80)

    class Meta(Base.Meta):
        ordering = Base.Meta.ordering + ["label"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.label


class Tag(Base):
    """
    Represents a tag available in system.
    """

    label = models.CharField(unique=True, max_length=80)

    def __str__(self):
        return f"#{self.label}"


class CommonTag(Base):
    tags = models.ManyToManyField(
        Tag,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta(Base.Meta):
        abstract = True


class Course(CommonTag):
    """
    Represents a course available in system.
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="courses",
        help_text="Category of the course.",
    )
    # instructor = models.ForeignKey(
    #     InstructorProxy,
    #     on_delete=models.CASCADE,
    #     help_text="The instructor or teacher assigned to teach the course.",
    # )

    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to="courses/%Y/%m/%d/",
        default=None,
        null=True,
        blank=True,
        help_text="Upload banner of the course",
        storage=MediaCloudinaryStorage(),
    )

    class Meta(CommonTag.Meta):
        unique_together = ("category", "title")

    @admin.display(description="Thumbnail")
    def thumbnail(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.image.url}" alt="{self.title}" title="{self.title}" width="80" height="80" class="img-thumbnail rounded shadow" />'
            )

    def __str__(self):
        return self.title
