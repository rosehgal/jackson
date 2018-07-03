#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Jackson module.

This module does all the translations from the jackson (The extension of JSON)
type file to json file. The extension offered in package, allows the value of
JSON to be resolved at runtime.

For now it only supports env variables and call to the functions returning
strings.
"""


__date__ = '28 June 2018'
__author__ = ('Rohit Sehgal <rsehgal@cse.iitk.ac.in>')


from typing import Any
from importlib import import_module

import re
import os
import builtins
import traceback
import sre_compile

Match = type(sre_compile.compile('', 0).match(''))  # cf. Lib/re.py#L263


class REResolver:
    """
    This class defines how the values from the jackson file will be translated
    to in memory json (having secrets) file.

    For now it supports translations from either environment variables or from
    other python functions. Which are specified in MATCH_REGEX

    The key value have to be declared like:
        - env.<ENVIRONMENT_VAR_NAME>
        - !foo.bar.baz: the python notation of calling method from other python
            file.
    """
    def __init__(self) -> None:
        """
        Create a object that will perform, regex match/replace upon call.
        """
        self.MATCH_REGEX = '(env\.\w*)|(!\w*[\.\w]*)'
        # This regex will match something like:
        # env.FOO
        # !foo.bar.baz

        self._re = re.compile(self.MATCH_REGEX)

    @staticmethod
    def _resolve(m: Match) -> str:
        """
        This method will be called after match to one of the groups
        specified in MATCH_REGEX. Since for now, MATCH_REGEX only contains two
        groups, one for resolution to the environment variables and other is
        call to some other python functions.

        This function is very much dependent on MATCH_REGEX groups.
        """

        # for environment variables
        if m.groups()[0]:
            matched = m.groups()[0]
            env_var = matched[matched.find('.')+1:]
            return os.environ[env_var]
        # for calling functions
        else:
            matched = m.groups()[1]
            matched = matched[matched.find('!')+1:]
            function_name = matched[matched.rfind('.')+1]
            module_name = matched[:matched.rfind('.')]
            module = import_module(module_name)
            f = getattr(module, function_name)
            return f()

    def resolve(self, data: str) -> str:
        """
        This function handles the task of resolving the data(string) by
        performing regex match of data with MATCH_REGEX.
        """
        return self._re.sub(REResolver._resolve, data)


class File:
    """
    This call represents basic file like object for jackson files.

    Jackson file are the extension of JSON files, with this extension one can
    save secret from JSON file environment variables and in the extended
    JSON(jackson) file, pass the reference to those environment variable. The
    reference to those environment variables takes place in memory.

    This extension is also pluggable, like if you have secrets stored in some
    HSM or remote servers then you can write a wrapper around the locations, and
    the location of those python wrapper(functions) which takes care of that.
    """

    def __init__(self, path: str, *args: Any, **kwargs: Any) -> None:
        """
        Initialize various class parameters and REResolver
        """
        self._file = builtins.open(path, *args, **kwargs)
        self._resolver = REResolver()

    def read(self, n_bytes: int = -1):
        """
        This function mimics the builtin file.read but with resolution.

        Arguments:
          n_bytes (int): The count of value read at once.
        """
        data = self._file.read(n_bytes)
        return self._resolver.resolve(data)

    def __enter__(self) -> 'File':
        return self

    def __exit__(self, exception_type: type, exception_value: Exception,
                 traceback: traceback) -> None:
        self._file.close()
        self._file = None

    @classmethod
    def open(cls, path: str, *args: Any, **kwargs: Any) -> 'File':
        """
        Function that will return jackson file type object.
        """
        return cls(path, *args, **kwargs)
