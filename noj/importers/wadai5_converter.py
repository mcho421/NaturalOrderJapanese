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

ENTRY_HEADER = KANA_BLOCK('kana') + Optional(WIDE_NUMBER)('number') + \
    Optional(KANA_BLOCK + Optional(WIDE_NUMBER)) + Optional(KANJI_AND_CONTEXT_BLOCK) + \
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

NUMBERED_MEANING_HEADER = Optional(Literal(u'〜') + CharsNotIn(u' ') + 
                          Suppress(u' ')) + Word(nums)('dict_meaning_number') + \
                          SkipTo(lineEnd)('dict_meaning')
NUMBERED_MEANING_HEADER.leaveWhitespace()
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
SURPRISE_ENTRY_BODY_NUMBERED = Group(UNNUMBERED_MEANING_BLOCK) + \
                               OneOrMore(Group(NUMBERED_MEANING_BLOCK))
SURPRISE_ENTRY_BODY_NUMBERED.setParseAction(check_surprise_entry_body_numbered)

ENTRY_BODY = OneOrMore(Group(NUMBERED_MEANING_BLOCK))('numbered') | \
             SURPRISE_ENTRY_BODY_NUMBERED('numbered') | \
             Group(UNNUMBERED_MEANING_BLOCK)('unnumbered')

ENTRY_BLOCK = Group(ENTRY_HEADER)('entry_header') + Suppress(lineEnd) + \
              Group(ENTRY_BODY)('entry_body')

DIRTY_DATA = [
    (u'〔古代エジプトの王〕 1 【〜3 世】 Amenhotep', u'1 〔古代エジプトの王〕 【〜3 世】 Amenhotep'),
    (u'〔このように〕 1 thus; so; like this;', u'1 〔このように〕 thus; so; like this;'),
    (u'〜な 1 〔ひとりよがりな〕 complacent;', u'1 〜な 〔ひとりよがりな〕 complacent;'),
    (u'〜な 1 〔一方にだけ偏っている〕 one-sided;', u'1 〜な 〔一方にだけ偏っている〕 one-sided;'),
    (u'the palm (of the hand).', u'1 the palm (of the hand).'),
    (u'〜な 1 〔等級が低いさま〕 low-grade;', u'1 〜な 〔等級が低いさま〕 low-grade;'),
    (u'〜な 1 〔条件に合う〕 suitable;', u'1 〜な 〔条件に合う〕 suitable;'),
    (u'〜な 1 〔手で扱うのにちょうどよい〕 handy;', u'1 〜な 〔手で扱うのにちょうどよい〕 handy;'),
    (u'〜する 1 〔えぐってほじり出す〕 gouge out', u'1 〜する 〔えぐってほじり出す〕 gouge out'),
    (u'〜な[の] 1 〔出るがままの〕 unrestricted', u'1 〜な[の] 〔出るがままの〕 unrestricted'),
    (u'〜な 1 〔繊細な〕 sensitive;', u'1 〜な 〔繊細な〕 sensitive;'),
    (u'nature; 〔自生〕 spontaneity.', u'1 nature; 〔自生〕 spontaneity.'),
    (u'a finishing blow; 〖F〗', u'1 a finishing blow; 〖F〗'),
    (u'〜な 1 〔陽気な〕 lively;', u'1 〜な 〔陽気な〕 lively;'),
    (u'〜な 1 〔身体的〕 physical;', u'1 〜な 〔身体的〕 physical;'),
    (u'〜な[の] 〔突然の〕 sudden;', u'1 〜な[の] 〔突然の〕 sudden;'),
    (u'にわかに　1 〔突然に〕 suddenly;', u'2 にわかに　〔突然に〕 suddenly;'),
    (u'2 〔即座に〕 immediately;', u'3 〔即座に〕 immediately;'),
    (u'〜な 1 〔懇切・丁寧〕 polite;', u'1 〜な 〔懇切・丁寧〕 polite;'),
    (u'〜な 1 〔味や香りなどが濃いさま〕 thick;', u'1 〜な 〔味や香りなどが濃いさま〕 thick;'),
    (u'〖＜Port padre〗 1 〔宣教師〕', u'1 〖＜Port padre〗 〔宣教師〕'),
    (u'〔人・動物の〕 a nose;', u'1 〔人・動物の〕 a nose;'),
    (u'〖＜Port pão〗 1 bread.', u'1 〖＜Port pão〗 bread.'),
    (u'〖＜Du zontag〗 1 〔土曜日〕', u'1 〖＜Du zontag〗 〔土曜日〕'),
    (u'〜な[の] 〔過剰でない〕 moderate;', u'1 〜な[の] 〔過剰でない〕 moderate;'),
    (u'[⇒<LINK>ベルイマン</LINK[152273:938]>, <LINK>バーグマン</LINK[146712:1664]>] 1 Bergman', u'1 [⇒<LINK>ベルイマン</LINK[152273:938]>, <LINK>バーグマン</LINK[146712:1664]>] Bergman'),
    (u'〖＜Skt māra〗 1 〔仏道修行を妨げるもの〕', u'1 〖＜Skt māra〗 〔仏道修行を妨げるもの〕'),
    (u'〔円形の〕 round;', u'1 〔円形の〕 round;'),
    (u'〜な 〔すばらしい〕 wonderful;', u'1 〜な 〔すばらしい〕 wonderful;'),
    (u'a twist; a ply; a strand; a lay.', u'1 a twist; a ply; a strand; a lay.'),
    (u'〖＜F roman〗 1 〔散文物語・長篇小説〕', u'1 〖＜F roman〗 〔散文物語・長篇小説〕'),
    (u'＝<LINK>うきでる</LINK[113001:206]>. 1 〔表面に〕', u'1 ＝<LINK>うきでる</LINK[113001:206]>. 〔表面に〕'),
]
CHEAP_HACKS = [
    (u'70 年安保(闘争)　', u'・70 年安保(闘争)　'),
    (u'1 週労働時間数　*workweek;', u'・1 週労働時間数　*workweek;'),
    (u'4 輪[前輪]ディスクブレーキ', u'・4 輪[前輪]ディスクブレーキ'),
    (u'6 か月点検　a six-monthly', u'・6 か月点検　a six-monthly'),
    (u'1 位: 熾(し)天使 a seraph', u'・1 位: 熾(し)天使 a seraph'),
    (u'1 次 [2 次]電池　a primary', u'・1 次 [2 次]電池　a primary'),
    (u'[⇒<LINK>どういう</LINK[142356:1388]>, <LINK>どうか</LINK[142390:772]>, <LINK>どうした</LINK[142550:1268]>, <LINK>どうして</LINK[142556:554]>, <LINK>どうでも</LINK[142684:1470]>, <LINK>どうにか</LINK[142712:126]>, <LINK>どうにも(こうにも)</LINK[142717:1050]>, <LINK>どうのこうの</LINK[142730:38]>, <LINK>どうみても</LINK[142789:1684]>, <LINK>どうやら</LINK[142811:1736]>, etc.]\n', u''),
    (u'20 勝投手　a twenty-game winner.', u'・20 勝投手　a twenty-game winner.'),
    (u'2 軒長屋　a two-family house;', u'・2 軒長屋　a two-family house;'),
    (u'3 軒長屋　a row house', u'・3 軒長屋　a row house'),
    (u'25 年祭　the ⌐25th', u'・25 年祭　the ⌐25th'),
    (u'50 年祭　the ⌐50th', u'・50 年祭　the ⌐50th'),
    (u'100 年祭　the ⌐100th', u'・100 年祭　the ⌐100th'),
    (u'150 年祭　the ⌐150th', u'・150 年祭　the ⌐150th'),
    (u'200 年祭　the ⌐200th', u'・200 年祭　the ⌐200th'),
    (u'250 年祭', u'・250 年祭'),
    (u'300 年祭　the ⌐300th', u'・300 年祭　the ⌐300th'),
    (u'400 年祭　the ⌐400th', u'・400 年祭　the ⌐400th'),
    (u'500 年祭　the ⌐500th', u'・500 年祭　the ⌐500th'),
    (u'600 年祭　the ⌐600th', u'・600 年祭　the ⌐600th'),
    (u'700 年祭　the ⌐700th', u'・700 年祭　the ⌐700th'),
    (u'800 年祭　the ⌐800th', u'・800 年祭　the ⌐800th'),
    (u'900 年祭　the ⌐900th', u'・900 年祭　the ⌐900th'),
    (u'1000 年祭　the ⌐1000th', u'・1000 年祭　the ⌐1000th'),
    (u'【音楽】 〔音名〕 C. [⇒<LINK>ハちょうちょう</LINK[147486:1106]>, <LINK>ハたんちょう</LINK[147461:132]>]\n', u''),
    (u'(しいて訳せば in regard to などとできるが, 通例直接訳さない)\n', u''),
    (u'4 輪馬車　a four-wheeler;', u'・4 輪馬車　a four-wheeler;'),
    (u'8 ミリ・フィルム　8-mm film.', u'・8 ミリ・フィルム　8-mm film.'),
    (u'6[9]人制バレー(ボール)　six-[nine-]player', u'・6[9]人制バレー(ボール)　six-[nine-]player'),
    (u'〔ローマ教皇〕 Pius.\n', u''),
    (u'suddenness; unexpectedness.\n', u''),
    (u'⇒<LINK>まがった</LINK[153695:1640]>.\n', u''),
    (u'⇒<LINK>まとめあげる</LINK[154108:222]>.\n', u''),
    (u'＝<LINK>-よう２</LINK[157508:906]>.\n', u''),
    (u'⇒<LINK>わすれがち</LINK[159790:1912]>, <LINK>わすれさられる</LINK[159791:946]>, <LINK>わすれさる</LINK[159792:494]>.\n', u''),
    (u'35 ミリカメラ　a ⌐35-millimeter', u'・35 ミリカメラ　a ⌐35-millimeter'),
    (u'3D カメラ　〔立体カメラ〕', u'・3D カメラ　〔立体カメラ〕'),
    (u'100 メートル競走　the 100-meter', u'・100 メートル競走　the 100-meter'),
    (u'8 時間勤務　a shift', u'・8 時間勤務　a shift'),
    (u'5 年契約　《sign》', u'・5 年契約　《sign》'),
    (u'6 連発拳銃　a six-chambered', u'・6 連発拳銃　a six-chambered'),
    (u'5 分利付き公債　five-percent', u'・5 分利付き公債　five-percent'),
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
    print json.dumps(out, 
        sort_keys=True, indent=4, ensure_ascii=False)

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
    # i = 0
    e1 = 0
    # print dump_text[2855349:2895349]
    for t,s,e in ENTRY_BLOCK.scanString(dump_text):
        # i += 1
        # if i % 100 == 0:
        #     print (s,e)
        print (s,e)
        if s != e1:
            raise ValueError("Skipped something")
        print dump_text[s:e]
        print_entry(t)
        print 
        s1, e1 = s, e

def sanitize_dirty_data(text):
    for find, replace in DIRTY_DATA:
        text = text.replace(find, replace)
    for find, replace in CHEAP_HACKS:
        text = text.replace(find, replace)
    return text


def main():
    # dump_text = dedent(u"""\
    #     おとも【お供】 ﾛｰﾏ(otomo)
    #     ＝<LINK>とも２</LINK[143623:308]>.
    #     〜する 〔随行する〕 attend; accompany; 〔同行する〕 go [come] with….
    #     ▲社長にお供してヨーロッパを回ってきた.　I accompanied the president around Europe.
    #     おどらす１, おどらせる１【踊らす, 踊らせる】 ﾛｰﾏ(odorasu, odoraseru)
    #     〔人を意のままに操る〕 manipulate; lead sb into…; pull the strings.
    #     ▲母親が彼女を陰で踊らせているのだ.　Her mother is manipulating her behind the scenes.
    #     おどらす２, おどらせる２【躍らす, 躍らせる】 ﾛｰﾏ(odorasu, odoraseru)
    #     1 〔勢いよく体を投げ出す〕
    #     ▲彼はがけの上から海に身を躍らせた.　He ⌐hurled [cast, flung, threw] himself off the cliff into the sea.
    #     2 〔心をわくわくさせる〕
    #     ▲彼女は入賞の喜びに胸を躍らせて表彰式に臨んだ.　Thrilled [Filled with excitement] at winning a prize, she went to the prize-giving ceremony.
    #     """)
    # dump_text = sanitize_dirty_data(dump_text)

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
    parse_dump_file('kendump.txt', skip_lines=185330)
    # parse_dump_file('kendump.txt')

if __name__ == '__main__':
    main()
