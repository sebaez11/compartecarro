# Django
from django.db import models


class BaseModel(models.Model):
    """This is a Base Model that every model of a project's app
    is going to extend for inheriting information about times.

    :attribute created_at: Datetime that the object is created.
    :attribute modified_at: Recent datetime that the object is modified.
    """
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']