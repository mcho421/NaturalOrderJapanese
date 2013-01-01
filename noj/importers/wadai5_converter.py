#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
import pprint
from pyparsing import *
from textwrap import dedent
import pdb

class UniPrinter(pprint.PrettyPrinter):
    """Pretty print lists and dicts containing unicode properly."""
    def pprint(self, object):
        if isinstance(object, str):
            unesc = unicode(object, 'unicode-escape')
        elif isinstance(object, unicode):
            unesc = unicode(object.encode('unicode-escape').\
                replace('\\\\u', '\\u'), 'unicode-escape')
        else:
            unesc = unicode(str(self.pformat(object)), 'unicode-escape')
        print unesc

pp = UniPrinter(indent=4)

def entry_number_to_int(t):
    return int(t[0])

def split_kanji(t):
    joined = ' '.join(t[0])
    return ParseResults(joined.split(u'・'))

def join_romaji(t):
    raw_tokens = t[0][0]
    str_tokens = list()
    for t in raw_tokens:
        if isinstance(t, ParseResults):
            str_tokens.append('(')
            str_tokens.append(t[0])
            str_tokens.append(')')
        else:
            str_tokens.append(t)
    return ''.join(str_tokens)

def join_expression(t):
    return ''.join(t)

# Parsing entry headers
WIDE_NUMBER = Word(u'０１２３４５６７８９')
WIDE_NUMBER.setParseAction(entry_number_to_int)

ROMA_SYMBOL = Literal(u' ﾛｰﾏ').leaveWhitespace()
KANJI_BLOCK = nestedExpr(opener=u'【', closer=u'】')
KANJI_BLOCK.setParseAction(split_kanji)

CONTEXT_BLOCK = Suppress(u' 【') + SkipTo(u'】') + Suppress(u'】')
CONTEXT_BLOCK.leaveWhitespace()
CONTEXT_BLOCK.setParseAction(lambda t : t[0])

KANJI_AND_CONTEXT_BLOCK = OneOrMore(CONTEXT_BLOCK('context') | 
                          KANJI_BLOCK('kanji'))

KANA_BLOCK = SkipTo(WIDE_NUMBER, failOn=lineEnd) | \
             SkipTo(KANJI_AND_CONTEXT_BLOCK, failOn=lineEnd) | \
             SkipTo(ROMA_SYMBOL, failOn=lineEnd)
KANA_BLOCK.leaveWhitespace()

ROMAJI_BLOCK = Group(nestedExpr(opener=u'(', closer=u')', 
                                content=CharsNotIn(u'()')))
ROMAJI_BLOCK.setParseAction(join_romaji)

ENTRY_HEADER = KANA_BLOCK('kana') + Optional(WIDE_NUMBER)('number') + \
    Optional(KANA_BLOCK) + Optional(KANJI_AND_CONTEXT_BLOCK) + \
    Optional(CONTEXT_BLOCK)('context') + Suppress(ROMA_SYMBOL) + \
    ROMAJI_BLOCK('romaji')
ENTRY_HEADER.leaveWhitespace()

# Parsing entry bodies
END_PUNCTUATION = oneOf(u'. 」 ! ?')
END_EXPRESSION = END_PUNCTUATION + Literal(u'　')
EXPRESSION = SkipTo(END_EXPRESSION, failOn=lineEnd) + END_PUNCTUATION
EXPRESSION.leaveWhitespace()
EXPRESSION.setParseAction(join_expression)
SENTENCE_MEANING = SkipTo(lineEnd)
SENTENCE_MEANING.leaveWhitespace()
EXAMPLE_SENTENCE = Optional(oneOf(u'▲ ・ ◧ ◨')) + EXPRESSION('expression') + \
                   Literal(u'　') + SENTENCE_MEANING('meaning')
EXAMPLE_SENTENCE.leaveWhitespace()

PHRASE_EXPRESSION = SkipTo(u'　', failOn=lineEnd) | SkipTo(lineEnd)
EXAMPLE_PHRASE = Optional(oneOf(u'▲ ・ ◧ ◨')) + \
                 PHRASE_EXPRESSION('expression') + ((Suppress(u'　') + \
                 SkipTo(lineEnd)('meaning')) | SkipTo(lineEnd))

NUMBERED_MEANING_HEADER = Word(nums)('dict_meaning_number') + \
                          SkipTo(lineEnd)('dict_meaning')
NOT_USAGE_EXAMPLE = ~(NUMBERED_MEANING_HEADER | ENTRY_HEADER)
USAGE_EXAMPLE = NOT_USAGE_EXAMPLE + (Group(EXAMPLE_SENTENCE)('sentence') | 
                                     Group(EXAMPLE_PHRASE)('phrase'))
NUMBERED_MEANING_BLOCK = Group(NUMBERED_MEANING_HEADER)('meaning_header') + \
                         Suppress(lineEnd) + ZeroOrMore(Group(USAGE_EXAMPLE) + 
                                              Suppress(lineEnd))('usage_examples')
UNNUMBERED_MEANING_HEADER = SkipTo(lineEnd)('dict_meaning')
UNNUMBERED_MEANING_BLOCK = Group(UNNUMBERED_MEANING_HEADER)('meaning_header') + \
                         Suppress(lineEnd) + ZeroOrMore(Group(USAGE_EXAMPLE) + 
                                              Suppress(lineEnd))('usage_examples')

ENTRY_BODY = OneOrMore(Group(NUMBERED_MEANING_BLOCK))('numbered') | \
             Group(UNNUMBERED_MEANING_BLOCK)('unnumbered')

ENTRY_BLOCK = Group(ENTRY_HEADER)('ENTRY_HEADER') + Suppress(lineEnd) + \
              Group(ENTRY_BODY)('entry_body')

def print_entry(parsed_entry):
    out = dict()
    out['header'] = parsed_entry['ENTRY_HEADER'].asDict()
    if 'kanji' in out['header']:
        k = out['header']['kanji']
        out['header']['kanji'] = k.asList()
    if 'numbered' in parsed_entry['entry_body']:
        meanings = parsed_entry['entry_body']['numbered']
    elif 'unnumbered' in parsed_entry['entry_body']:
        meanings = [parsed_entry['entry_body']['unnumbered']]

    mlist = list()
    for m in meanings:
        ues = list()
        if 'usage_examples' in m:
            for ue in m['usage_examples']:
                ue_dict = ue.asDict()
                for key in ue_dict:
                    ue_dict[key] = ue_dict[key].asDict()
                ues.append(ue_dict)
        mlist_item = {'dict_meaning':m['meaning_header']['dict_meaning']}
        if len(ues) > 0: mlist_item['usage_examples'] = ues
        mlist.append(mlist_item)
    out['meanings'] = mlist
    print json.dumps(out, 
        sort_keys=True, indent=4, ensure_ascii=False)

def main():
    with codecs.open("kendump.txt", 'r', 'utf-8') as myfile:
        head=[myfile.next().rstrip() for x in xrange(100)]
    dump_text = '\n'.join(head)

    e1 = 0
    for t,s,e in ENTRY_BLOCK.scanString(dump_text):
        print (s,e)
        if s != e1:
            raise ValueError("Skipped something")
        print dump_text[s:e]
        print_entry(t)
        print 
        s1, e1 = s, e

if __name__ == '__main__':
    main()
