from django.db import models

class Clock(models.Model):
    """
    Clock model
    """
    clocked_in = models.DateTimeField(auto_now_add=True)
    clocked_out = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)

