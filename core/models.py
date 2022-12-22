from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    conf = models.JSONField()
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return self.name


class Pair(BaseModel):
    account = models.ForeignKey(
        'core.Account', on_delete=models.CASCADE, related_name='pairs')
    name = models.CharField(max_length=55, unique=True)
    quantity_precision = models.IntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
