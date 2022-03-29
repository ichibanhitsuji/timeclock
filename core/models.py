from django.db import models

class Clock(models.Model):
    """
    Clock model
    """
    clocked_in = models.DateTimeField(auto_now_add=True)
    clocked_out = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.id

