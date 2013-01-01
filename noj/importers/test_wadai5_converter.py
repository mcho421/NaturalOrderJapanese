#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import unittest
from textwrap import dedent
import wadai5_converter as c

class TestWadai5Converter(unittest.TestCase):

    def test_ENTRY_HEADERs(self):
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
            あいわす, あいわする【相和す, 相和する】 ﾛｰﾏ(aiwasu, aiwasuru)
            あいそ２, あいそう【愛想】 ﾛｰﾏ(aiso, aisō)
            「ああ, 荒野」 ﾛｰﾏ(aa, kōya)
            あし２【蘆, 葦】 ﾛｰﾏ(ashi)
            あったか, あったかい, あったかさ, あったまる, あっためる, etc. ﾛｰﾏ(attaka, attakai, attakasa, attamaru, attameru)
            """).splitlines()

        for entry in test_entries:
            print entry
            d = c.ENTRY_HEADER.parseString(entry).dump()
            c.pp.pprint(d)
            print

    def test_sentences(self):
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

        for entry in test_sentences:
            print entry
            d = c.EXAMPLE_SENTENCE.parseString(entry).dump()
            c.pp.pprint(d)
            print

    def test_phrases(self):
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
            ああ言えばこう言う
            〜する *ground; ″earth.
            """).splitlines()

        for entry in test_phrases:
            print entry
            d = c.EXAMPLE_PHRASE.parseString(entry).dump()
            c.pp.pprint(d)
            print

    def test_bodies(self):
        test_bodies = [
            dedent(u"""\
                1 〔問いに答えて〕
                ・「眠くないか」「ああ, 眠くない」　"Aren't you sleepy?"―"No, I'm not."
                ▲でかした(ぞ)!　Well done! ｜ Bravo! ｜ Wonderful! ｜ Good for you!
                アーチ橋　an arch bridge.
                ▲ああいうふうに　(in) that way; like that; so.
                2 〔気軽な肯定・承諾〕
                ▲「これ借りていいですか」「ああ, いいよ」　"Can I borrow this?"―"Yes, all right [《口》 Yeah, OK]."
                """),
            dedent(u"""\
                that sort of 《person》; 《a man》 like that; such 《people》.
                ・「眠くないか」「ああ, 眠くない」　"Aren't you sleepy?"―"No, I'm not."
                ▲でかした(ぞ)!　Well done! ｜ Bravo! ｜ Wonderful! ｜ Good for you!
                アーチ橋　an arch bridge.
                ▲ああいうふうに　(in) that way; like that; so.
                """),
        ]

        for body in test_bodies:
            print body
            d = c.ENTRY_BODY.parseString(body).dump()
            c.pp.pprint(d)
            print
            
    def test_entries(self):
        test_entries = [
            dedent(u"""\
                ああいう ﾛｰﾏ(aaiu)
                that sort of 《person》; 《a man》 like that; such 《people》.
                ▲ああいうふうに　(in) that way; like that; so."""),
            dedent(u"""\
                アース ﾛｰﾏ(āsu)
                【電】 *ground; ″earth.
                〜する *ground; ″earth.
                ▲アースしてある　*be grounded; ″be earthed.
                ▲洗濯機にアースを取りつける　〔アース線をアース端子につなぐ〕 connect the ⌐*ground wire [lead] of the washing machine to the terminal; *ground [″earth] the washing machine
                ・感電防止のためかならずアースをしてください.　Please be sure to ⌐*ground [″earth] the equipment, to avoid the danger of electric shock.
                ◧アース線　*a ground wire; ″an earthed line.
                アース板　*a ground [″an earth] plate.
                """),
        ]

        for entry in test_entries:
            print entry
            d = c.ENTRY_BLOCK.parseString(entry).dump()
            c.pp.pprint(d)
            print

    def test_multi_entries(self):
        test_multi_entries = [
            dedent(u"""\
                ああ１ ﾛｰﾏ(aa)
                1 〔問いに答えて〕
                ▲「お父さん, あれなあに」「ああ, あれは灯台だよ」　"What is that, Daddy?"―"Oh, it is a lighthouse."
                2 〔気軽な肯定・承諾〕
                ▲「これ借りていいですか」「ああ, いいよ」　"Can I borrow this?"―"Yes, all right [《口》 Yeah, OK]."
                ・「眠くないか」「ああ, 眠くない」　"Aren't you sleepy?"―"No, I'm not."
                ああいう ﾛｰﾏ(aaiu)
                that sort of 《person》; 《a man》 like that; such 《people》.
                ▲ああいうふうに　(in) that way; like that; so.
                アーヴィン ﾛｰﾏ(āvin)
                Ervine, St. John (Greer) (1883-1971; アイルランドの劇作家・小説家).
                """),
            dedent(u"""\
                あいそ１【哀訴】 ﾛｰﾏ(aiso)
                an appeal; an entreaty; a petition; a complaint. [＝<LINK>あいがん１</LINK[108301:392]>]
                〜する appeal; make an appeal 《to…》; implore; entreat; petition; complain.
                あいそ２, あいそう【愛想】 ﾛｰﾏ(aiso, aisō)
                1 〔人にいい感じを与えようとする気持ちや態度〕 friendliness; 《文》 affability; 《文》 amiability.
                ▲愛想よく　pleasantly; in a friendly way; affably; amiably; 〔店員などが〕 helpfully
                ・愛想よくする　try to be ⌐friendly [helpful, amiable, affable] to [toward] sb; make oneself ⌐agreeable [pleasant] to [toward] sb
                """),
        ]

        for multi_entry in test_multi_entries:
            e1 = 0
            for t,s,e in c.ENTRY_BLOCK.scanString(multi_entry):
                print (s,e)
                if s != e1:
                    raise ValueError("Skipped something")
                print multi_entry[s:e]
                c.print_entry(t)
                print 
                s1, e1 = s, e
                

if __name__ == '__main__':
    unittest.main()
