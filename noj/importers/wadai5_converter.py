#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *
from textwrap import dedent
import pdb
import pprint

class UniPrinter(pprint.PrettyPrinter):
    """Pretty print lists and dicts containing unicode properly."""
    def pprint(self, object):
        unesc = unicode(str(self.pformat(object)), 'unicode-escape')
        print unesc

pp = UniPrinter(indent=4)

kana_block = Regex('bleh')
entry_number = Word(u'０１２３４５６７８９')
kanji_block = Suppress(u'【') + CharsNotIn(u'】') + Suppress(u'】')
# entry_header = kana_block + entry_number + 

test_entries = dedent(u"""\
    私""").splitlines()

# entry_number.parseString(u"私１")
# pp.pprint(entry_number.parseString(u"１"))
# pp.pprint(entry_number.parseString(u"０１"))

