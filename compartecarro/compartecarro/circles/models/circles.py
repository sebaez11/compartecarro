# Django
from django.db import models

# Utils
from compartecarro.utils.models import BaseModel


class Circle(BaseModel):

    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)

    members = models.ManyToManyField(
        "users.User", 
        through="circles.Membership",
        through_fields=('circle', 'user')
    )

    # Statistics
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(
        'verified circle',
        default=False,
        help_text='Verified circles are also known as official communities'
    )

    is_public = models.BooleanField(default=True)
    is_limited = models.BooleanField(default=False)
    members_limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        
        ordering = ['-rides_taken', '-rides_offered']