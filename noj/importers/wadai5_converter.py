#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from pyparsing import *
from textwrap import dedent
import pdb
import pprint

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
        # unesc = unicode(str(self.pformat(object)), 'unicode-escape')
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


entry_number = Word(u'０１２３４５６７８９')
entry_number.setParseAction(entry_number_to_int)

roma_symbol = Literal(u' ﾛｰﾏ').leaveWhitespace()
kanji_block = nestedExpr(opener=u'【', closer=u'】')
kanji_block.setParseAction(split_kanji)

# context_block = Suppress(u' ') + nestedExpr(opener=u'【', closer=u'】')
context_block = Suppress(u' 【') + SkipTo(u'】') + Suppress(u'】')
context_block.leaveWhitespace()
context_block.setParseAction(lambda t : t[0])

kanji_and_context_block = OneOrMore(context_block('context') | 
                          kanji_block('kanji'))

kana_block = SkipTo(entry_number) | SkipTo(kanji_and_context_block) | \
             SkipTo(roma_symbol)
kana_block.leaveWhitespace()
romaji_block = Group(nestedExpr(opener=u'(', closer=u')', 
                                content=CharsNotIn(u'()')))
romaji_block.setParseAction(join_romaji)
# kanji_block = Suppress(u'【') + CharsNotIn(u'】') + Suppress(u'】')
# entry_header = kana_block + entry_number + 
entry_header = kana_block('kana') + Optional(entry_number)('number') + \
    Optional(kanji_and_context_block) + Optional(context_block)('context') + \
    Suppress(roma_symbol) + romaji_block('romaji')
entry_header.leaveWhitespace()

tmp = u' 【薬 】 ﾛｰﾏ'
d = context_block.parseString(tmp).dump()
pp.pprint(d)

test_entries = dedent(u"""\
    ああ１ ﾛｰﾏ(aa)
    ああ２ ﾛｰﾏ(aa)
    ああ３ ﾛｰﾏ(aa)
    ああいう ﾛｰﾏ(aaiu)
    アーク【ARC】 ﾛｰﾏ(āku)
    アークとう【アーク灯】 ﾛｰﾏ(ākutō)
    「ああ, 荒野」 ﾛｰﾏ(aa, kōya)
    アーサーおうでんせつ【アーサー王伝説】 ﾛｰﾏ(āsāōdensetsu)
    「アーサー・サヴィル卿の犯罪」 ﾛｰﾏ(āsā・savirukyōnohanzai)
    アース・カラー ﾛｰﾏ(āsu・karā)
    アーチトップ(ギター) ﾛｰﾏ(āchitoppu(gitā))
    アーティスティック・インプレッション ﾛｰﾏ(ātisutikku・inpuresshon)
    アーパネット【ARPANET】 ﾛｰﾏ(āpanetto)
    アール１【R】 ﾛｰﾏ(āru)
    アール・アイりょうほう【RI 療法】 ﾛｰﾏ(āru・airyōhō)
    アール・アンド・ディー【R ＆ D】 ﾛｰﾏ(āru・ando・dī)
    アール・エス・にさんにシー【RS-232C】 ﾛｰﾏ(āru・esu・nisannishī)
    アール・エスひょうじほう【RS 表示法】 ﾛｰﾏ(āru・esuhyōjihō)
    アイアン(クラブ) ﾛｰﾏ(aian(kurabu))
    アイ・オー【I/O】 ﾛｰﾏ(ai・ō)
    あいがき(つぎ)【相欠き(継ぎ)】 ﾛｰﾏ(aigaki(tsugi))
    アイこうか【I 効果】 ﾛｰﾏ(aikōka)
    アイデア, アイディア ﾛｰﾏ(aidea, aidia)
    アイ・ピー【IP】 【電算】 ﾛｰﾏ(ai・pī)
    あいわす, あいわする【相和す, 相和する】 ﾛｰﾏ(aiwasu, aiwasuru)
    アウター(ウエア) ﾛｰﾏ(autā(uea))
    「赤頭巾(ちゃん)」 ﾛｰﾏ(akazukin(chan))
    あかむし【赤虫】 【動】 ﾛｰﾏ(akamushi)
    -あがり【-上がり】 ﾛｰﾏ(-agari)
    あく４【開く・明く・空く】 ﾛｰﾏ(aku)
    あく５【飽く】 ﾛｰﾏ(aku)
    あつでん【圧電】 【電】 ﾛｰﾏ(atsuden)
    えんしがい【遠紫外】 【物・光】 ﾛｰﾏ(enshigai)
    ゲストノロン 【薬】 ﾛｰﾏ(gesutonoron)
    ジアステレオ 【化】 ﾛｰﾏ(jiasutereo)
    (-)ならない, (-)ならぬ ﾛｰﾏ((-)naranai, (-)naranu)
    """).splitlines()

for entry in test_entries:
    print entry
    d = entry_header.parseString(entry).dump()
    pp.pprint(d)
    print

# entry_number.parseString(u"私１")
# pp.pprint(entry_number.parseString(u"１"))
# pp.pprint(entry_number.parseString(u"０１"))

