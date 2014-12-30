from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=4096)
    content = models.TextField()
    smp_input = models.TextField() # sample input
    smp_output = models.TextField() # sample output


class Code(models.Model):
    LANG_TYPE_CHOICES = (
        ('cpp', 'C++'),
        ('text', 'plain text'),
    )
    RESULT_CHOICES = {
        ('CE', 'compiling error'),
        ('EE', 'executing error'),
        ('OK', 'success'),
        ('PD', 'task pending'),
    }
    SUFFIX_DIR = {
        'cpp': 'cpp',
        'text': 'txt',
    }
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    lang_type = models.CharField(max_length=128, choices=LANG_TYPE_CHOICES)
    content = models.TextField()
    compile_result = models.CharField(max_length=16, choices=RESULT_CHOICES, default='PD')
    compile_msg = models.TextField()
    exec_result = models.CharField(max_length=16, choices=RESULT_CHOICES)
    exec_msg = models.TextField()

    @property
    def suffix(self):
        return '.' + self.SUFFIX_DIR.get(self.lang_type)
