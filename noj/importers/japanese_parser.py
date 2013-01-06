#!/usr/bin/env python
# -*- coding: utf-8 -*-

# code adapted from:
# http://mecab.googlecode.com/svn/trunk/mecab/doc/bindings.html
# https://github.com/dae/ankiplugins/blob/master/japanese/reading.py

import MeCab
import re
from jcconv import *

BOS_EOS = 0
INTERJECTION = 1
ADVERB = 2
PRE_NOUN_ADJECTIVAL = 3
NOUN = 4
AUXILIARY_VERB = 5
VERB = 6
PARTICLE = 7
PREFIX = 8
ADJECTIVE = 9
CONJUNCTION = 10
FILLER = 11
SYMBOL = 12
OTHER = 13

MORPHEME_TYPES = {
    u'BOS/EOS':BOS_EOS,
    u'感動詞':INTERJECTION,
    u'副詞':ADVERB,
    u'連体詞':PRE_NOUN_ADJECTIVAL,
    u'名詞':NOUN,
    u'助動詞':AUXILIARY_VERB,
    u'動詞':VERB,
    u'助詞':PARTICLE,
    u'接頭詞':PREFIX,
    u'形容詞':ADJECTIVE,
    u'接続詞':CONJUNCTION,
    u'フィラー':FILLER,
    u'記号':SYMBOL,
    u'その他':OTHER,
}

class JapaneseParser(object):
    """A MeCab parser to parse japanese sentences into morphemes."""

    def __init__(self):
        super(JapaneseParser, self).__init__()
        self._parser = None
        self.skipTypes = frozenset([BOS_EOS])

    def parse(self, expression):
        """Parse a Japanese expression into morphemes. 
        
        Args:
            expression: A Unicode string representing a Japanese
                expression.

        Returns:
            An instance of JapaneseParseResults containing the 
            expression parsed into morphemes.
        """
        expression_utf8 = expression.encode('utf-8')
        node = self.parser.parseToNode(expression_utf8)
        results = JapaneseParseResults()
        results.expression_unicode = expression
        results.expression_utf8 = expression_utf8
        position = 0
        while node:
            feature = unicode(node.feature, encoding='utf-8')
            details = re.split(',', feature)
            for d in range(0,len(details)):
                if details[d] == '*':
                    details[d] = ''
            type = MORPHEME_TYPES[details[0]]
            if type not in self.skipTypes:
                morpheme = unicode(node.surface, encoding='utf-8')
                utf8_pos = (node.rlength-node.length)+position
                unicode_pos = len(unicode(expression_utf8[0:utf8_pos], encoding='utf-8'))
                results.add_morpheme (
                    morpheme=morpheme,
                    base=details[-3],
                    reading=kata2hira(details[-2]),
                    length=len(morpheme),
                    position=unicode_pos,
                    type=type
                )
            position = position + node.rlength
            node = node.next
        return results

    @property
    def parser(self):
        """Get the Japanese parser by lazy instantiation."""
        if not self._parser:
            self._parser = MeCab.Tagger('mecabrc')
        return self._parser

class JapaneseParseResults(object):
    """Contains morphemes from parsing using JapaneseParser."""
    def __init__(self):
        super(JapaneseParseResults, self).__init__()
        self.expression_utf8 = None
        self.expression_unicode = None
        self.morphemes = list()
        self.skipTypesComponents = frozenset([BOS_EOS, SYMBOL])
        self._components = None

    def add_morpheme(self, morpheme, base=None, reading=None, 
                     length=None, position=None, type=None):
        """Add a morpheme to the parse results."""
        m = {
            'morpheme':morpheme,
            'base':base,
            'reading':reading,
            'length':length,
            'position':position,
            'type':type,
        }
        self.morphemes.append(m)

    @property
    def components(self):
        """Return list of morpheme data for populating the database.

        Ignores punctuation.
        
        Returns:
            A list of morpheme data (dicts) corresponding to the 
            breakup of a Japanese expression. For example:

            [{'morpheme':u'今日', 'base':u'今日', 'reading': 
                u'きょう', 'position': 0, 'length': 6, 
                'type':NOUN}, 
            {'morpheme':u'も', 'base':u'も', 'reading': 
                u'も', 'position': 6, 'length': 3, 
                'type':PARTICLE}]
        """
        if self._components == None:
            self._components = list()
            for m in self.morphemes:
                if m['type'] not in self.skipTypesComponents:
                    self._components.append(m)
        return self._components

def listDictString(l):
    """Used for pretty printing japanese parse result components
    as directly printing out the data structure will not display
    utf-8 correctly"""
    out = list()
    for item in l:
        group = ['{']
        for key, value in item.items():
            valuePrint = value
            if not isinstance(value, int):
                valuePrint = "'{}'".format(value.encode('utf-8'))
            group.append("'{}':{}, ".format(key, valuePrint))
        group.append('},')
        out.append(''.join(group))
    return '\n'.join(out)

        
if __name__ == "__main__":
    parser = JapaneseParser()
    # results = parser.parse(u"明日は晴れるかな")
    #results = parser.parse(u"自動 生成されています.")
    #results = parser.parse(u"自動 生成されています.")
    #results = parser.parse(u"今日もしないとね。")
    #results = parser.parse(u'明日は今日よりやや暖かいでしょう.')
    #results = parser.parse(u'プログラムは一部2,000 円だ.')
    #results = parser.parse(u'データは以下のとおりです。')
    #results = parser.parse(u'This is english')
    results = parser.parse(u"　明日は　　晴れるかな")
    #print (results.components)
    print(listDictString(results.components))
