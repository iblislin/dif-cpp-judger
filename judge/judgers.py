import os
import subprocess

from subprocess import check_call, check_output
from tempfile import NamedTemporaryFile
from uuid import uuid4

from celery import Task
from django.conf import settings

from .models import Achievement, Code


class BaseJudgerTask(Task):
    ignore_result = True
    abstract = True

    def run(self, code):
        """
        :type code: Code
        """
        self.code = code
        self._create_tmpfile()

    def _create_tmpfile(self):
        self._tmpfile = NamedTemporaryFile(suffix=self.code.suffix, dir=settings.JUDGE_DIR)
        self._tmpfile.file.write(self.code.content)
        self._tmpfile.file.close()

    def _check_output(self, *args, **kwargs):
        _stderr = kwargs.pop('stderr', subprocess.STDOUT)
        return check_output(stderr=_stderr, *args, **kwargs)


class CppJudgerTask(BaseJudgerTask):
    compiler = '/usr/bin/clang++'

    def run(self, code):
        super(CppJudgerTask, self).run(code)
        self._outfile = self._tmpfile.name.rstrip(self.code.suffix)

        try:
            # compile
            self.code.compile_msg = self._check_output([self.compiler,
                '-o', self._outfile, self._tmpfile.name])

            try:
                # exectue
                self.code.exec_msg = self._check_output([self._outfile])
                # check answer
                if self.code.exec_msg == self.code.question.test_answer.rstrip():
                    self.code.status = 'AC'
                    ach, _created = Achievement.objects.get_or_create(user=self.code.user,
                        question=self.code.question,
                        defaults={'code_id': self.code.id}
                        )
                    if not _created:
                        ach.code = self.code
                        ach.save()
                else:
                    self.code.status = 'WA'
            except subprocess.CalledProcessError as e:
                self.code.exec_msg = e.output
                self.code.status = 'EE'

        except subprocess.CalledProcessError as e:
            self.code.compile_msg = e.output
            self.code.status = 'CE'


        self.code.save()
