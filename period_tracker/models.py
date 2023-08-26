from django.db import models
from django.contrib.auth.models import User

class Period(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_day = models.DateField()
    ovulation_day = models.DateField(null=True)

    class Meta:
        unique_together = ["user", "first_day"]

    def __str__(self):
        return str(self.first_day)
    