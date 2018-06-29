#!/usr/bin/env python3


"""Jackson module.

This module does all the translations from the jackson (The extension of JSON)
type file to json file. The extension offered in package, allows the value of
JSON to be resolved at runtime.

For now it only supports env variables and call to the functions returning
strings.

"""


__date__ = '28 June 2018'
__author__ = ('Rohit Sehgal <rsehgal@cse.iitk.ac.in>')


import re
import os
import builtins
from importlib import import_module


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
    def __init__(self):
        """
        Create a object that will perform, regex match/replace upon call.
        """
        self.MATCH_REGEX = '(env.\w*)|(!\w*[\.\w]*)'
        # This regex will match something like:
        # env.FOO
        # !foo.bar.baz

        self._re = re.compile(self.MATCH_REGEX)

    @staticmethod
    def _resolve(m):

        """
        This method will be called after match to one of the groups
        specified in MATCH_REGEX. Since for now, MATCH_REGEX only contains two
        groups, one for resolution to the environment variables and other is
        call to some other python functions.

        This function is very much dependent on MATCH_REGEX groups.

        Arguments:
          m (SRE_Match): The result of re.match() or re.search.
        Return:
          string: resolved values of env or of function call.
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

    def resolve(self, data):
        """
        This function handles the task of resolving the data(string) by
        performing regex match of data with MATCH_REGEX.

        Arguments:
          data (string): Input to test/replace with MATCH_REGEX.
        Return:
          string: after resolution
        """
        return self._re.sub(REResolver._resolve, data)


class File(object):
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

    def __init__(self, path, *args, **kwargs):
        """
        Initialize various class parameters and REResolver
        """
        self._file = builtins.open(path, *args, **kwargs)
        self._resolver = REResolver()

    def read(self, n_bytes=-1):
        """
        This function mimics the builtin file.read but with resolution.

        Arguments:
          n_bytes (int): The count of value read at once.
        """
        data = self._file.read(n_bytes)
        return self._resolver.resolve(data)

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, e_tb):
        self._file.close()
        self._file = None


def open(path, *args, **kwargs):
    """
    Function that will return jackson file type object.
    """
    return File(path, *args, **kwargs)
