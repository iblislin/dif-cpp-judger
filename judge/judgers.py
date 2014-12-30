import os
import subprocess

from subprocess import check_call, check_output
from tempfile import NamedTemporaryFile
from uuid import uuid4

from celery import Task
from django.conf import settings

from .models import Code


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

    def _compile(self):
        self._outfile = self._tmpfile.name.rstrip(self.code.suffix)
        try:
            output = self._check_output([self.compiler,
                '-o', self._outfile, self._tmpfile.name])
            self.code.compile_result = 'OK'
        except subprocess.CalledProcessError as e:
            output = e.output
            self.code.compile_result = 'CE'

        self.code.compile_msg = output

    def _exec(self):
        if self.code.compile_result != 'OK':
            return
        try:
            output = self._check_output([self._outfile])
            self.code.exec_result = 'OK'
        except subprocess.CalledProcessError as e:
            output = e.output
            self.code.compile_result = 'EE'

        self.code.exec_msg = output

    def run(self, code):
        super(CppJudgerTask, self).run(code)
        self._compile()
        self._exec()
        self.code.save()
