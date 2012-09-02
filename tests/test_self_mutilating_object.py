#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from self_mutilating_object import SelfMutilatingObject


@pytest.mark.nondestructive
class TestSelfMutilatingObject(object):

    def test_init(self):

        smobj = SelfMutilatingObject(a='a string', b=42, c=3.14)

        assert smobj.a == 'a string'
        assert smobj.b == 42
        assert smobj.c == 3.14

    def test_add_method_args(self):

        smobj = SelfMutilatingObject()
        smobj.add_method('multiply', lambda a, b: a * b)

        assert smobj.multiply(2, 2) == 4

    def test_add_method_params(self):
        smobj = SelfMutilatingObject()

        def concat(*params):
            concat = ""
            for word in params:
                if concat:
                    concat + " and "
                concat += word
            return concat

        smobj.add_method('concatinate', concat)

        smobj.concatinate('one', 'two', 'three') == "one and two and three"

    def test_add_method_kwargs(self):
        smobj = SelfMutilatingObject()
        
        def translate(**kwargs):
            answer = ""
            for (k, v) in kwargs.items():
                if answer:
                    answer += ", "
                answer += "%s %s" % (v, k)
            return answer

        smobj.add_method('translate', translate)

        answer = smobj.translate(cat='siamese', dog='terrier', mouse='field')
        assert "siamese cat" in answer
        assert "terrier dog" in answer
        assert "field mouse" in answer


    def test_add_method_name_exception(self):
        smobj = SelfMutilatingObject()
        def thing():
            print "thing works"

        exception = None
        try:
            smobj.add_method(42, thing)
        except TypeError as exception:
            pass
        assert exception

    def test_add_method_coderef_exception(self):
        smobj = SelfMutilatingObject()
        exception = None
        try:
            smobj.add_method('walla', 'walla')
        except TypeError as exception:
            pass
        assert exception
