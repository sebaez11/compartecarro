# Django
from django.db import models

# Utilities
from compartecarro.utils.models import BaseModel

# Managers
from compartecarro.circles.managers import InvitationManager


class Invitation(BaseModel):

    code = models.CharField(max_length=50, unique=True)

    issued_by = models.ForeignKey(
        "users.User", 
        on_delete=models.CASCADE,
        help_text='Circle member that is providing the invitation',
        related_name='issued_by'
    )
    used_by = models.ForeignKey(
        "users.User", 
        on_delete=models.CASCADE,
        null=True,
        help_text='User that used the code to enter the circle'
    )

    circle = models.ForeignKey("circles.Circle", on_delete=models.CASCADE)

    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True)

    objects = InvitationManager()

    def __str__(self):
        return f'#{self.circle.slug_name}; {self.code}'