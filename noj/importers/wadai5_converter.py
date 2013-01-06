#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
import pprint
import re
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

def check_surprise_entry_body_numbered(t):
    if t[1]['meaning_header']['dict_meaning_number'] != '2':
        raise ParseException("dict_meaning_number should be 2")

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

ENTRY_HEADER_MATCHER = re.compile(ur' ﾛｰﾏ')
ENTRY_HEADER = KANA_BLOCK('kana') + Optional(WIDE_NUMBER)('number') + \
    Optional(KANA_BLOCK + Optional(WIDE_NUMBER)) + Optional(KANJI_AND_CONTEXT_BLOCK) + \
    Optional(CONTEXT_BLOCK)('context') + Suppress(SkipTo(ROMA_SYMBOL, failOn=lineEnd)) + \
    Suppress(ROMA_SYMBOL) + ROMAJI_BLOCK('romaji')
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

NUMBERED_MEANING_MATCHER = re.compile(r'(\d+) ') # move to top later
NUMBERED_MEANING_HEADER = Optional(Literal(u'〜') + CharsNotIn(u' \n') + 
                          Suppress(u' ')) + Word(nums)('dict_meaning_number') + \
                          Suppress(u' ') + SkipTo(lineEnd)('dict_meaning')
NUMBERED_MEANING_HEADER.leaveWhitespace()
NOT_USAGE_EXAMPLE = (NUMBERED_MEANING_HEADER | ENTRY_HEADER)
USAGE_EXAMPLE = (Group(EXAMPLE_SENTENCE)('sentence') | 
                 Group(EXAMPLE_PHRASE)('phrase'))
USAGE_EXAMPLE_IN_BLOCK = ~NOT_USAGE_EXAMPLE + Group(USAGE_EXAMPLE)

NUMBERED_MEANING_BLOCK = Group(NUMBERED_MEANING_HEADER)('meaning_header') + \
                         Suppress(lineEnd) + \
                         ZeroOrMore(USAGE_EXAMPLE_IN_BLOCK +
                                    Suppress(lineEnd))('usage_examples')
UNNUMBERED_MEANING_HEADER = SkipTo(lineEnd)('dict_meaning')
UNNUMBERED_MEANING_BLOCK = Group(UNNUMBERED_MEANING_HEADER)('meaning_header') + \
                           Suppress(lineEnd) + \
                           ZeroOrMore(USAGE_EXAMPLE_IN_BLOCK +
                                      Suppress(lineEnd))('usage_examples')
SURPRISE_ENTRY_BODY_NUMBERED = Group(UNNUMBERED_MEANING_BLOCK) + \
                               OneOrMore(Group(NUMBERED_MEANING_BLOCK))
SURPRISE_ENTRY_BODY_NUMBERED.setParseAction(check_surprise_entry_body_numbered)

LINK_LINE = oneOf(u'[⇒ ＝ ⇒') + Literal(u'<LINK>') + SkipTo(lineEnd)

ENTRY_BODY = Optional(LINK_LINE + lineEnd) + \
             OneOrMore(Group(NUMBERED_MEANING_BLOCK))('numbered') | \
             SURPRISE_ENTRY_BODY_NUMBERED('numbered') | \
             Group(UNNUMBERED_MEANING_BLOCK)('unnumbered')

ENTRY_BLOCK = Group(ENTRY_HEADER)('entry_header') + Suppress(lineEnd) + \
              Group(ENTRY_BODY)('entry_body')

DIRTY_DATA = [
    (u'ごぶがゆ【五分粥】 ﾛｰﾏ', u'ごぶがゆ【五分粥】 ﾛｰﾏ(gobugayu)'),
]

def format_entry(parsed_entry):
    out = dict()
    out['header'] = parsed_entry['entry_header'].asDict()
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
    return out

def print_entry(parsed_entry):
    out = format_entry(parsed_entry)
    print get_json(out)

def get_json(serializable):
    return json.dumps(serializable, sort_keys=True, indent=4, 
                      ensure_ascii=False)


def sanitize_dirty_data(text):
    for find, replace in DIRTY_DATA:
        text = text.replace(find, replace)
    return text

def fix_numbered_meanings(entry_text):
    uses_numbered_meanings = False
    lines = entry_text.split('\n')
    potential_numbered_meanings = list()
    for i in xrange(1, len(lines)):
        m = NUMBERED_MEANING_MATCHER.match(lines[i])
        if m:
            number_lino_tuple = (int(m.group(0)), i)
            potential_numbered_meanings.append(number_lino_tuple)

    if potential_numbered_meanings:
        f_number = potential_numbered_meanings[0][0]
        f_number_lino = potential_numbered_meanings[0][1]
        has_link_line = LINK_LINE.searchString(lines[1])
        potential_start_linos = [1]
        if has_link_line: potential_start_linos.append(2)

        if f_number == 1 and f_number_lino in potential_start_linos:
            uses_numbered_meanings = True
        if f_number == 2 and f_number_lino != 1:
            uses_numbered_meanings = True

    if uses_numbered_meanings == False:
        for num, lino in potential_numbered_meanings:
            lines[lino] = u'・' + lines[lino]
    else:
        next_number = f_number
        for num, lino in potential_numbered_meanings:
            if num != next_number:
                lines[lino] = u'・' + lines[lino]
            else:
                next_number += 1

    return '\n'.join(lines)

def split_into_entries(text):
    entries = list()
    entry_buffer = list()
    lines = text.split('\n')
    for line in lines:
        is_entry_header = ENTRY_HEADER_MATCHER.search(line)
        if is_entry_header and entry_buffer:
            entry_lines = '\n'.join(entry_buffer)
            entries.append(entry_lines)
            entry_buffer = list()
        entry_buffer.append(line)
    entry_lines = '\n'.join(entry_buffer)
    entries.append(entry_lines)
    return entries

def parse_entry(entry_text):
    sanitized_entry = fix_numbered_meanings(entry_text)
    block = ENTRY_BLOCK + stringEnd
    d = block.parseString(sanitized_entry)
    return format_entry(d)

def parse_multiple_entries(text):
    entries = split_into_entries(text)
    converted_entries = list()
    for entry in entries:
        print entry
        d = parse_entry(entry)
        converted_entries.append(d)
    return converted_entries

def parse_dump_file(dump_file, num_lines=None, skip_lines=None):
    with codecs.open(dump_file, 'r', 'utf-8') as myfile:
        if isinstance(num_lines, int):
            head = [myfile.next().rstrip() for x in xrange(num_lines)]
        else:
            head = myfile.read().splitlines()
        if isinstance(skip_lines, int):
            head = head[skip_lines:-1]
    dump_text = '\n'.join(head)
    dump_text = sanitize_dirty_data(dump_text)

    print len(dump_text)
    parsed_entries = parse_multiple_entries(dump_text)
    return get_json(parsed_entries)

class Wadai5Converter(object):
    """Convert Kenkyusha 5th EPWING Dictionary dump to importable format."""
    def __init__(self, dumpfile, outfile=None):
        super(Wadai5Converter, self).__init__()
        self.dumpfile = dumpfile
        self.outfile  = outfile
        self.entries  = None
        self.converted_entries = None

    def initialize_entries(self):
        with codecs.open(self.dumpfile, 'r', 'utf-8') as myfile:
            head = myfile.read().splitlines()
        dump_text = '\n'.join(head)
        dump_text = sanitize_dirty_data(dump_text)
        self.entries = split_into_entries(dump_text)

    def get_num_entries(self):
        if self.entries is None:
            self.initialize_entries()
        return len(self.entries)

    def convert_generator(self):
        if self.entries is None:
            self.initialize_entries()
        self.converted_entries = list()
        for i, entry in enumerate(self.entries):
            # print entry
            d = parse_entry(entry)
            self.converted_entries.append(d)
            yield i
        if self.outfile is not None:
            with codecs.open(self.outfile, 'w', 'utf-8') as myfile:
                # myfile.write(get_json(self.converted_entries)) # Memory error
                for c_entry in self.converted_entries:
                    myfile.write(get_json(c_entry))
                    myfile.write('\n\n')


def main():
    # dump_text = dedent(u"""\
    #     a time ⌐slip [warp]; time travel.
    #     〜する
    #     ▲それは主人公が 50 年後の未来にタイム・スリップする映画だ.　It's a movie in which the hero travels through a time warp 50 years into the future.
    #     ・江戸時代にタイム・スリップしたような気がする　feel as if one had been transported through time to the Edo period
    #     ・その町を歩くと 100 年前のヨーロッパにタイム・スリップしたような気になる.　When I walk through that town I feel as though I were a time-traveler in the Europe of a hundred years ago.
    #     """)
    # dump_text = sanitize_dirty_data(dump_text)
    # tmp = u'〜する'
    # print UNNUMBERED_MEANING_BLOCK.parseString(dump_text).dump()
    # exit()

    test_multi_entries = [
        dedent(u"""\
            ああいう ﾛｰﾏ(aaiu)
            that sort of 《person》; 《a man》 like that; such 《people》.
            ▲ああいうふうに　(in) that way; like that; so.
            あんぽ【安保】 ﾛｰﾏ(anpo)
            ＝<LINK>あんぜんほしょう</LINK[110208:562]>.
            ▲安保反対!　〔デモ隊のシュプレヒコール〕 Down with the Security Pact!
            ◨食糧安保　the guaranteed security of foodstuffs.
            70 年安保(闘争)　the demonstrations against the renewal of the Japan-US Security Treaty in 1970.
            ◧安保改定　revision of the (Japan-US) Security Treaty.
            """),
        dedent(u"""\
            いっしゅう(かん)【一週(間)】 ﾛｰﾏ(isshū(kan))
            a week.
            ◧1 週 5 日制　a five-day workweek.
            1 週労働時間数　*workweek; ″working week.
            ディスク・ブレーキ ﾛｰﾏ(disuku・burēki)
            〔自動車などの円板ブレーキ〕 a ⌐disc [disk] brake.
            ◨ベンチレーテッド・ディスクブレーキ　a ⌐ventilated [vented] disc brake.
            4 輪[前輪]ディスクブレーキ　《be equipped with》 ⌐four-wheel [front] disc brakes.
            """),
        dedent(u"""\
            ゴーグル ﾛｰﾏ(gōguru)
            〔防護めがね〕 (a pair of) goggles; (水泳用) (swimming) goggles.
            ◨スキー・ゴーグル　snow [ski] goggles.
            3D ゴーグル　〔三次元映像用の〕 3-D goggles.
            ながや【長屋】 ﾛｰﾏ(nagaya)
            *a row house; *a tenement (house); ″a terrace(d) house.
            ▲長屋住まいをする, 長屋に住む　live in a row house.
            2 軒長屋　a two-family house; *a duplex (house); ″a semidetached house.
            3 軒長屋　a row house divided into three units.
            ◧長屋造りの　built in ⌐row-house [″terrace-house] style; 〔安普請の〕 jerry-built.
            """),
        dedent(u"""\
            どう７ ﾛｰﾏ(dō)
            [⇒<LINK>どういう</LINK[142356:1388]>, <LINK>どうか</LINK[142390:772]>, <LINK>どうした</LINK[142550:1268]>, <LINK>どうして</LINK[142556:554]>, <LINK>どうでも</LINK[142684:1470]>, <LINK>どうにか</LINK[142712:126]>, <LINK>どうにも(こうにも)</LINK[142717:1050]>, <LINK>どうのこうの</LINK[142730:38]>, <LINK>どうみても</LINK[142789:1684]>, <LINK>どうやら</LINK[142811:1736]>, etc.]
            1 〔状態や意見をたずねる〕 how; what.
            ▲〔あいさつで〕 どう, 調子は.　How are things [How's life] with you? ｜ How's ⌐things [everything]?
            2 〔勧める・誘う・提案する〕 how about.
            ▲コーヒーでもどう.　Will you have a (cup of) coffee?
            どう７ ﾛｰﾏ(dō)
            [⇒<LINK>どういう</LINK[142356:1388]>, <LINK>どうか</LINK[142390:772]>, <LINK>どうした</LINK[142550:1268]>, <LINK>どうして</LINK[142556:554]>, <LINK>どうでも</LINK[142684:1470]>, <LINK>どうにか</LINK[142712:126]>, <LINK>どうにも(こうにも)</LINK[142717:1050]>, <LINK>どうのこうの</LINK[142730:38]>, <LINK>どうみても</LINK[142789:1684]>, <LINK>どうやら</LINK[142811:1736]>, etc.]
            1 〔状態や意見をたずねる〕 how; what.
            3 ▲〔あいさつで〕 どう, 調子は.　How are things [How's life] with you? ｜ How's ⌐things [everything]?
            2 〔勧める・誘う・提案する〕 how about.
            ▲コーヒーでもどう.　Will you have a (cup of) coffee?
            """),
    ]

    # for multi_entry in test_multi_entries:
    #     print multi_entry
    #     parsed_entries = parse_multiple_entries(multi_entry)
    #     print get_json(parsed_entries)
    #     print

    # print dump_text
    # d = ENTRY_BLOCK.parseString(dump_text)
    # pp.pprint(d.dump())
    # print_entry(d)

    # e1 = 0
    # for t,s,e in ENTRY_BLOCK.scanString(dump_text):
    #     print (s,e)
    #     if s != e1:
    #         raise ValueError("Skipped something")
    #     print dump_text[s:e]
    #     print_entry(t)
    #     print 
    #     s1, e1 = s, e

    # TODO: maybe write parse action to check whether numbered meaning is in order, or then UE
    # parse_dump_file('kendump.txt', skip_lines=336224)
    # parse_dump_file('kendump.txt')
    # converter = Wadai5Converter('kendump_small.txt', 'kenconvert_small.txt')
    converter = Wadai5Converter('kendump.txt', 'kenconvert.txt')
    num_entries = converter.get_num_entries()

    import progressbar as pb
    widgets = ['Converting: ', pb.Percentage(), ' ', pb.Bar(),
               ' ', pb.Timer(), ' ']
    pbar = pb.ProgressBar(widgets=widgets, maxval=num_entries).start()

    for i in converter.convert_generator():
        pbar.update(i)
    pbar.finish()
    # print get_json(converter.converted_entries)

if __name__ == '__main__':
    main()
