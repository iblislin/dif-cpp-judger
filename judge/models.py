from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=4096)
    content = models.TextField()


class Code(models.Model):
    LANG_TYPE_CHOICES = (
        ('cpp', 'C++'),
        ('text', 'plain text'),
    )
    SUFIX_DIR = {
        'cpp': 'cpp',
        'text': 'txt',
    }
    user = models.ForeignKey(User)
    lang_type = models.CharField(max_length=128, choices=LANG_TYPE_CHOICES)
    content = models.TextField()
    smp_input = models.TextField() # sample input
    smp_output = models.TextField() # sample output
    exec_result = models.TextField()

    @property
    def sufix(self):
        return self.SUFIX_DIR.get(self.lang_type)
