#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class SelfMutilatingObject(object):
    '''A Class that can have attributes initialized with kwargs and add methods.'''

    def __init__(self, **kwargs):
        '''SelfMutilatingObject constructor. Initializes object with attributes based on keyword arguments.
        '''
        for k, v in kwargs.items():
            # self.__dict__[k] = v
            object.__setattr__(self, k, v)

    def add_method(self, name, coderef):
        '''Adds method to self.

        ::Args::
        - name - string without whitespace to be used as method name
        - coderef - function reference

        '''

        def function():
            pass
        if type(name) != type('string'):
            raise TypeError, "Parameter 'name' must be of type string."
        if type(coderef) != type(function):
            raise TypeError, "Parameter 'coderef' must be a function reference."
        object.__setattr__(self, name, coderef)

