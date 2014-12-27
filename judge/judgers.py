import os
import subprocess

from abc import ABCMeta, abstractmethod
from subprocess import check_call, check_output
from uuid import uuid4

from django.conf import settings

from .models import Code


class BaseJudger(object):
    __metaclass__ = ABCMeta

    def __init__(self, code):
        """
        :type code: Code
        """
        self.code = code
        self._create_tmp_file(code.sufix)

    def _create_tmp_file(self, sufix):
        self._filename = '{uuid}{sufix}'.format(uuid=uuid4(),
            sufix= '.' + sufix if sufix else ''
            )
        self._filepath = os.path.join(settings.JUDGE_DIR, self._filename)
        with open(self._filepath) as f:
            f.write(self.code.content)

    def __del__(self):
        try:
            os.remove(self._filepath)
        except Exception as e:
            pass

    @abstractmethod
    def run(self):
        pass

    def _check_output(self, *args, **kwargs):
        _stderr = kwargs.pop('stderr', subprocess.STDOUT)
        return check_output(*args, **kwargs, stderr=_stderr)


class CppJudger(BaseJudger):
    compiler = '/usr/bin/clang++'

    def _compile(self):
        try:
            output = self._check_output([self.compiler,
                '-o', self._filepath, self._filepath])
        except subprocess.CalledProcessError as e:
            output = e.output
        return output

    def run(self):
        self._compile()
