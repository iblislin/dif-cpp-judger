import os
import subprocess

from subprocess import check_call, check_output, Popen, PIPE
from tempfile import NamedTemporaryFile
from uuid import uuid4

from celery import Task
from celery.exceptions import SoftTimeLimitExceeded
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

    def _popen(self, *args, **kwargs):
        return Popen(stdout=PIPE, stderr=PIPE, stdin=PIPE,
            universal_newlines=True, *args, **kwargs)


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
                # execute
                _p = self._popen([self._outfile])
                _output, _error = _p.communicate(self.code.question.test_data)
                if _error:
                    self.code.exec_msg = _error
                    self.code.status = 'EE'
                    raise subprocess.CalledProcessError('Code: {0} executing error'.format(self.code.id))
                # check answer
                _output = unicode(_output.rstrip())
                self.code.exec_msg = _output
                _answer = self.code.question.test_answer.rstrip().replace('\r', '')
                if _output == _answer:
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
                print e
            except SoftTimeLimitExceeded as e:
                raise e

        except subprocess.CalledProcessError as e:
            self.code.compile_msg = e.output
            self.code.status = 'CE'
        except SoftTimeLimitExceeded as e:
            self.code.status = 'TO'

        self.code.save()
