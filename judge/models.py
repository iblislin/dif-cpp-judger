from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=4096)
    content = models.TextField()
    smp_input = models.TextField(null=True, blank=True) # sample input
    smp_output = models.TextField(null=True, blank=True) # sample output
    test_data = models.TextField(null=True, blank=True)
    test_answer = models.TextField(null=True)

    def __unicode__(self):
        return self.title


class Code(models.Model):
    LANG_TYPE_CHOICES = (
        ('cpp', 'C++'),
        ('text', 'plain text'),
    )
    STATUS_CHOICES = {
        ('AC', 'Acceptance'),
        ('CE', 'Compiling error'),
        ('EE', 'Executing error'),
        ('PD', 'Task pending'),
        ('TO', 'Timeout'),
        ('WA', 'Wrong answer'),
    }
    STATUS_DIR = dict(STATUS_CHOICES)
    SUFFIX_DIR = {
        'cpp': 'cpp',
        'text': 'txt',
    }
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    lang_type = models.CharField(max_length=128, choices=LANG_TYPE_CHOICES)
    content = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='PD')
    compile_msg = models.TextField(null=True)
    exec_msg = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def suffix(self):
        return '.' + self.SUFFIX_DIR.get(self.lang_type)

    def get_status(self):
        return self.STATUS_DIR.get(self.status)

    def __unicode__(self):
        return u'#{qid} {user} {status}'.format(qid=self.question.id,
            user=self.user.username,
            status=self.status,
            )


class Achievement(models.Model):
    user = models.ForeignKey(User)
    code = models.ForeignKey(Code)
    question = models.ForeignKey(Question)

    @property
    def is_pass(self):
        """
        :return: get the latest AC code, if not return false
        """
        d = self.code.objects.filter(user_id=self.user.id, status='AC')[:1]
        if d:
            return d
        else:
            return False

    def __unicode__(self):
        return '#{question} {user} {code}'.format(
                question=self.question.title,
                user=self.user.username,
                code=self.code.id,
            )
