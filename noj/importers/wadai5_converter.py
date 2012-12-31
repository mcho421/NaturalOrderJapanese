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

def join_expression(t):
    return ''.join(t)

# Parsing entry headers
entry_number = Word(u'０１２３４５６７８９')
entry_number.setParseAction(entry_number_to_int)

roma_symbol = Literal(u' ﾛｰﾏ').leaveWhitespace()
kanji_block = nestedExpr(opener=u'【', closer=u'】')
kanji_block.setParseAction(split_kanji)

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

entry_header = kana_block('kana') + Optional(entry_number)('number') + \
    Optional(kanji_and_context_block) + Optional(context_block)('context') + \
    Suppress(roma_symbol) + romaji_block('romaji')
entry_header.leaveWhitespace()

# Parsing entry bodies
end_punctuation = oneOf(u'. 」 ! ?')
end_expression = end_punctuation + Literal(u'　')
expression = SkipTo(end_expression) + end_punctuation
expression.leaveWhitespace()
expression.setParseAction(join_expression)
meaning = SkipTo(stringEnd)
meaning.leaveWhitespace()
example_sentence = Optional(oneOf(u'▲ ・ ◧ ◨')) + expression('expression') + \
                   Literal(u'　') + meaning('meaning')
example_sentence.leaveWhitespace()

phrase_expression = SkipTo(u'　') | SkipTo(stringEnd)
example_phrase = Optional(oneOf(u'▲ ・ ◧ ◨')) + \
                 phrase_expression('expression') + Optional(Suppress(u'　') + \
                 SkipTo(stringEnd)('meaning'))

# tmp = u'▲ああいうふうに　(in) that way; like that; so.'
# tmp = u'◧アーチ形'
# d = example_phrase.parseString(tmp).dump()
# pp.pprint(d)

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

# for entry in test_entries:
#     print entry
#     d = entry_header.parseString(entry).dump()
#     pp.pprint(d)
#     print

test_sentences = dedent(u"""\
    ▲「お父さん, あれなあに」「ああ, あれは灯台だよ」　"What is that, Daddy?"―"Oh, it is a lighthouse."
    ▲「これ借りていいですか」「ああ, いいよ」　"Can I borrow this?"―"Yes, all right [《口》 Yeah, OK]."
    ▲選手たちがアーチをくぐって入場してきた.　The athletes marched under the arch and into the stadium.
    ▲どうしようもない虚脱感におそわれた.　I was assailed by a feeling of deep despondency. ｜ I was overwhelmed by a terrible sense of emptiness.
    ・その音で彼はぎょっとした.　The noise startled him. ｜ He started at the noise.
    ▲近くにおいでの際は拙宅にもお立ち寄りください.　Please ⌐call on us [drop in to see us] whenever you're in town.
    ・次の仕事の話は今手がけているのが終わってからにしてくれ.　Let me hear about the next job after I've finished with the one I'm working on now. ｜ Tell me about the next commission after I've finished with the one I'm on now.
    ▲お出かけですか.　Are you going ⌐somewhere [out]? ｜ You are ⌐leaving [heading off somewhere], are you?
    ▲でかした(ぞ)!　Well done! ｜ Bravo! ｜ Wonderful! ｜ Good for you!
    """).splitlines()

# for entry in test_sentences:
#     print entry
#     d = example_sentence.parseString(entry).dump()
#     pp.pprint(d)
#     print

test_phrases = dedent(u"""\
    ▲ああいうふうに　(in) that way; like that; so.
    ▲アーチをかける　hit [swat, loft] a home run.
    ◨馬蹄形アーチ　【建】 a horseshoe arch.
    ◧アーチ形
    ▲アーチ形の　《an entrance》 in the ⌐shape [form] of an arch; arch-shaped 《windows》; 【植】 fornicate 《leaves》.
    アーチ橋　an arch bridge.
    アーチ・ダム　an arch(ed) dam.
    ◧IH 炊飯器　an ⌐induction [IH] rice cooker.
    IH 調理器　an ⌐induction [IH] cooktop [cooker].
    ILO 代表　a 《Japanese》 delegate to the ILO.
    ▲手枷足枷をはめられて　in ⌐fetters [chains, shackles, irons]; fettered; shackled
    """).splitlines()

for entry in test_phrases:
    print entry
    d = example_phrase.parseString(entry).dump()
    pp.pprint(d)
    print

test_bodies = list()
test_bodies.append(dedent("""\
    ああ１ ﾛｰﾏ(aa)
    1 〔問いに答えて〕
    ▲「お父さん, あれなあに」「ああ, あれは灯台だよ」　"What is that, Daddy?"―"Oh, it is a lighthouse."
    2 〔気軽な肯定・承諾〕
    ▲「これ借りていいですか」「ああ, いいよ」　"Can I borrow this?"―"Yes, all right [《口》 Yeah, OK]."
    ・「眠くないか」「ああ, 眠くない」　"Aren't you sleepy?"―"No, I'm not."
    """))

# for body in test_bodies:
#     print body
