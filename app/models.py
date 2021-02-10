from django.db import models
from datetime import datetime, timedelta
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.exceptions import ValidationError
# Create your models here.


class Object(models.Model):
    name = models.CharField(null=False, max_length=255)


class Alias(models.Model):
    alias = models.CharField(null=False, max_length=255)
    target = models.ForeignKey(Object, db_constraint=False, on_delete=models.DO_NOTHING, max_length=24)
    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField(null=True)

    '''
    Overwriting save() method wih duplicated alias check.
    If instance with the same alias name, target object is running (end=Null),
    function will raise ValidationError. Otherwise, save object.
    '''
    def save(self, *args, **kwargs):
        duplicated_alias = Alias.objects.filter(Q(alias=self.alias), Q(target=self.target), Q(end__isnull=True))
        if duplicated_alias.exists():
            raise ValidationError("Same active alias exists.")
        else:
            super(Alias, self).save(*args, **kwargs)

    '''
    to_end_alias() function updates Alias object with current datetime,
    the last microsecond is non-inclusive
    '''
    def to_end_alias(self, *args, **kwargs):
        end = datetime.now() - timedelta(microseconds=1)
        self.end = end
        super(Alias, self).save(*args, **kwargs)
        return self.end
