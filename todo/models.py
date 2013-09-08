from string import uppercase

from django.db import models
from django.contrib.auth.models import User
from tastypie.models import create_api_key


nullable = ({'null': True, 'blank': True})


class TodoItem(models.Model):
    text = models.CharField(verbose_name='Description', max_length=256)
    completed = models.BooleanField(verbose_name='Completed')
    due = models.DateField(verbose_name='Due date', **nullable)
    priority = models.CharField(verbose_name='Priority', max_length=1, choices=zip(*[list(uppercase)]*2), help_text='e.g: A, B, C, ...', **nullable)
    user = models.ForeignKey(User, verbose_name='Author')

    def __unicode__(self):
        return self.text


models.signals.post_save.connect(create_api_key, sender=User)
