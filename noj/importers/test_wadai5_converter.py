#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import unittest
from textwrap import dedent
import pyparsing as p
import wadai5_converter as c

class TestWadai5Converter(unittest.TestCase):

    def test_entry_headers(self):
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
            おどらす１, おどらせる１【踊らす, 踊らせる】 ﾛｰﾏ(odorasu, odoraseru)
            """).splitlines()

        for entry in test_entries:
            print entry
            # entry = c.sanitize_dirty_data(entry)
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
            # entry = c.sanitize_dirty_data(entry)
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
            # entry = c.sanitize_dirty_data(entry)
            d = c.EXAMPLE_PHRASE.parseString(entry).dump()
            c.pp.pprint(d)
            print

    # def test_bodies(self):
    #     test_bodies = [
    #         dedent(u"""\
    #             1 〔問いに答えて〕
    #             ・「眠くないか」「ああ, 眠くない」　"Aren't you sleepy?"―"No, I'm not."
    #             ▲でかした(ぞ)!　Well done! ｜ Bravo! ｜ Wonderful! ｜ Good for you!
    #             アーチ橋　an arch bridge.
    #             ▲ああいうふうに　(in) that way; like that; so.
    #             2 〔気軽な肯定・承諾〕
    #             ▲「これ借りていいですか」「ああ, いいよ」　"Can I borrow this?"―"Yes, all right [《口》 Yeah, OK]."
    #             """),
    #         dedent(u"""\
    #             that sort of 《person》; 《a man》 like that; such 《people》.
    #             ・「眠くないか」「ああ, 眠くない」　"Aren't you sleepy?"―"No, I'm not."
    #             ▲でかした(ぞ)!　Well done! ｜ Bravo! ｜ Wonderful! ｜ Good for you!
    #             アーチ橋　an arch bridge.
    #             ▲ああいうふうに　(in) that way; like that; so.
    #             """),
    #     ]

    #     for body in test_bodies:
    #         print body
    #         body = c.sanitize_dirty_data(body)
    #         d = c.ENTRY_BODY.parseString(body).dump()
    #         c.pp.pprint(d)
    #         print
            
    def test_entries(self):
        print "TESTING ENTRIES"

        test_entries = [
            dedent(u"""\
                ああいう ﾛｰﾏ(aaiu)
                that sort of 《person》; 《a man》 like that; such 《people》.
                ▲ああいうふうに　(in) that way; like that; so.
                """),
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
            dedent(u"""\
                めいすい【名水】 ﾛｰﾏ(meisui)
                〔飲み水〕 (a) famed mineral water; 〔河川〕 a famous river; a renowned beautiful stream.
                ◧名水百選　〔環境省による〕 100 famed mineral waters.
                """),
            dedent(u"""\
                てんし２【天使】 ﾛｰﾏ(tenshi)
                〔キリスト教などで, 神の使い〕 an angel; a heavenly messenger; 〈集合的に〉 the celestial hierarchy; the heavenly host; 〔9 階位の天使の第 9 位〕 an angel; 〔天使のような人〕 an angel 《of a girl》.
                ➡9 階位の天使の第 1 位から第 8 位までは次のとおり.
                1 位: 熾(し)天使 a seraph 《pl. 〜s, -phim》　2 位: 智天使 a cherub 《pl. 〜s, -bim》　3 位: 座(ざ)天使 a throne　4 位: 主天使 a domination, a dominion　5 位: 力(りき)天使 a virtue　6 位: 能(のう)天使 a power　7 位: 権(げん)天使 a principality, a princedom　8 位: 大天使, 天使長 an archangel.
                ▲白衣の天使　a white angel; an angel dressed in white
                ▲天使の　angelic; seraphic; cherubic; cherublike
                ・天使のような　angelic 《smile》; seraphic
                ・天使のような女性　an angel of a woman
                ・天使のような子供の寝顔　the angelic face of a sleeping child
                ・天使の一群　a flight of angels; the host of heaven
                ・天使の階位　the celestial hierarchy; the angelic order
                ・天使の翼　angel(s') wings; angelic wings.
                ◨守護天使　a guardian angel.
                堕天使　a fallen angel; Lucifer.
                """),
            dedent(u"""\
                どう７ ﾛｰﾏ(dō)
                [⇒<LINK>どういう</LINK[142356:1388]>, <LINK>どうか</LINK[142390:772]>, <LINK>どうした</LINK[142550:1268]>, <LINK>どうして</LINK[142556:554]>, <LINK>どうでも</LINK[142684:1470]>, <LINK>どうにか</LINK[142712:126]>, <LINK>どうにも(こうにも)</LINK[142717:1050]>, <LINK>どうのこうの</LINK[142730:38]>, <LINK>どうみても</LINK[142789:1684]>, <LINK>どうやら</LINK[142811:1736]>, etc.]
                1 〔状態や意見をたずねる〕 how; what.
                ▲〔あいさつで〕 どう, 調子は.　How are things [How's life] with you? ｜ How's ⌐things [everything]?
                ・商売はどうですか.　How's your business? ｜ How is your business doing?
                ・〔病人に〕 今日はどうですか.　How ⌐do you feel [are you] today?
                ・京都はどうだった?　How were things in Kyoto? ｜ How did you like Kyoto?
                ・その小説はどうでしたか.　How did you find the novel? ｜ What did you think of the novel?
                ・君はあの男をどう思う.　What do you ⌐think [make] of him?
                2 〔勧める・誘う・提案する〕 how about.
                ▲コーヒーでもどう.　Will you have a (cup of) coffee?
                """),
            dedent(u"""\
                ベリマン ﾛｰﾏ(beriman)
                [⇒<LINK>ベルイマン</LINK[152273:938]>, <LINK>バーグマン</LINK[146712:1664]>] 1 Bergman, Torbern Olof (1735-84; スウェーデンの化学者).
                2 Berryman, John (1914-72; 米国の詩人).
                """),
            dedent(u"""\
                うきだす【浮き出す】 ﾛｰﾏ(ukidasu)
                ＝<LINK>うきでる</LINK[113001:206]>. 1 〔表面に〕 float to the surface; float up; come to the top.
                ▲やせて静脈が浮き出した腕　arms so thin that the veins ⌐stick out [swell up].
                ▲あまりの怒りに彼の額には血管が浮き出していた.　He got so angry that the ⌐veins [blood vessels] stood out on his forehead.
                2 〔目立つ〕 stand out.
                ▲ライトアップされた建物は暗闇の中で浮き出して見えた.　The brightly lit building stood out sharply in the surrounding darkness.
                """),
            dedent(u"""\
                ハ ﾛｰﾏ(ha)
                【音楽】 〔音名〕 C. [⇒<LINK>ハちょうちょう</LINK[147486:1106]>, <LINK>ハたんちょう</LINK[147461:132]>]
                ▲中央のハ(音)　middle C.
                """),
            dedent(u"""\
                どう７ ﾛｰﾏ(dō)
                [⇒<LINK>どういう</LINK[142356:1388]>, <LINK>どうか</LINK[142390:772]>, <LINK>どうした</LINK[142550:1268]>, <LINK>どうして</LINK[142556:554]>, <LINK>どうでも</LINK[142684:1470]>, <LINK>どうにか</LINK[142712:126]>, <LINK>どうにも(こうにも)</LINK[142717:1050]>, <LINK>どうのこうの</LINK[142730:38]>, <LINK>どうみても</LINK[142789:1684]>, <LINK>どうやら</LINK[142811:1736]>, etc.]
                1 〔状態や意見をたずねる〕 how; what.
                ▲〔あいさつで〕 どう, 調子は.　How are things [How's life] with you? ｜ How's ⌐things [everything]?
                2 〔勧める・誘う・提案する〕 how about.
                ▲コーヒーでもどう.　Will you have a (cup of) coffee?
                """),
            dedent(u"""\
                まがる【曲がる】 ﾛｰﾏ(magaru)
                ⇒<LINK>まがった</LINK[153695:1640]>.
                1 〔形が変わる〕 (弓状に) bend; arc; (くの字に) bend; make a 90-degree turn; 【解】 〔関節が動く〕 flex; 〔方向が変わる〕 turn; make a turn.
                ・ボールは大きく曲がってゴールを割った.　〔サッカーで〕 The ball made a big arc and made its way into the goal.
                2 〔道を折れる〕 make a ⌐bend [turn]; 〔カーブに沿う〕 turn; round.
                ▲左に曲がる　turn [strike] to the left (hand); turn left; take a left-hand turn 《on a road》
                """),
            dedent(u"""\
                ごーごー ﾛｰﾏ(gōgō)
                ＝<LINK>ごうごう２</LINK[125381:1794]>.
                ▲風が松林の中をごーごーと吹きわたった.　The wind roared ⌐among [through] the pine trees.
                ・列車が鉄橋をごーごーと渡っている.　The train is roaring across the bridge. ｜ There's a train roaring across the bridge.
                """),
            dedent(u"""\
                -みたい ﾛｰﾏ(-mitai)
                ＝<LINK>-よう２</LINK[157508:906]>.
                1 〔同じようだ〕 just like….
                ▲ライオンみたいな猫　a cat that's just like a lion.
                2 〔一例〕 like….
                ▲旅行はハワイみたいな所がいい.　For a vacation, a place like Hawaii would be good.
                """),
            dedent(u"""\
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
                """),
            dedent(u"""\
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
                """),
            dedent(u"""\
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
                """),
            dedent(u"""\
                どう７ ﾛｰﾏ(dō)
                [⇒<LINK>どういう</LINK[142356:1388]>, <LINK>どうか</LINK[142390:772]>, <LINK>どうした</LINK[142550:1268]>, <LINK>どうして</LINK[142556:554]>, <LINK>どうでも</LINK[142684:1470]>, <LINK>どうにか</LINK[142712:126]>, <LINK>どうにも(こうにも)</LINK[142717:1050]>, <LINK>どうのこうの</LINK[142730:38]>, <LINK>どうみても</LINK[142789:1684]>, <LINK>どうやら</LINK[142811:1736]>, etc.]
                1 〔状態や意見をたずねる〕 how; what.
                3 ▲〔あいさつで〕 どう, 調子は.　How are things [How's life] with you? ｜ How's ⌐things [everything]?
                2 〔勧める・誘う・提案する〕 how about.
                ▲コーヒーでもどう.　Will you have a (cup of) coffee?
                """),
            dedent(u"""\
                おすわり【お座り】 《小児語》 ﾛｰﾏ(osuwari)
                〜する sit down. [⇒<LINK>すわる１</LINK[134584:104]>]
                ▲きちんとお座りして食べなさい.　Sit (up) properly and eat your food.
                ・この人形はお座りもする抱き人形です.　This is a cuddly doll that can sit up, too.
                ▲赤ちゃんはお座りができるようになった.　The baby ⌐has learned to [is able to, can] sit up.
                ▲〔犬に向かって〕 お座り!　Sit!
                """),
            dedent(u"""\
                タイム・スリップ ﾛｰﾏ(taimu・surippu)
                a time ⌐slip [warp]; time travel.
                ▲それは主人公が 50 年後の未来にタイム・スリップする映画だ.　It's a movie in which the hero travels through a time warp 50 years into the future.
                ・江戸時代にタイム・スリップしたような気がする　feel as if one had been transported through time to the Edo period
                ・その町を歩くと 100 年前のヨーロッパにタイム・スリップしたような気になる.　When I walk through that town I feel as though I were a time-traveler in the Europe of a hundred years ago.
                """),
        ]

        for entry in test_entries:
            print entry
            print c.get_json(c.parse_entry(entry))
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
            dedent(u"""\
                あんぽ【安保】 ﾛｰﾏ(anpo)
                ＝<LINK>あんぜんほしょう</LINK[110208:562]>.
                ▲安保反対!　〔デモ隊のシュプレヒコール〕 Down with the Security Pact!
                ◨食糧安保　the guaranteed security of foodstuffs.
                70 年安保(闘争)　the demonstrations against the renewal of the Japan-US Security Treaty in 1970.
                ◧安保改定　revision of the (Japan-US) Security Treaty.
                安保堅持　the firm maintenance of the (Japan-US) Security Treaty.
                アンホイ【安徽】 ﾛｰﾏ(anhoi)
                ＝<LINK>あんき３</LINK[110149:88]>.
                """),
            dedent(u"""\
                いいき１【好い気】 ﾛｰﾏ(iiki)
                〜な 1 〔ひとりよがりな〕 complacent; self-satisfied; self-assured.
                ▲自分ひとりの力で成功したと思っているんだからいい気なものさ.　How conceited! The way he acts you'd think he'd done it all by himself.
                ・われわれの気遣いも知らないでいい気なものだ.　He is so wrapped up in himself that he's totally unaware of what we've done for him.
                2 〔得意〕
                ▲いい気になる　be ⌐vain [self-conceited, self-complacent, stuck-up]; be puffed up 《by [with]…》; puff oneself up 《with…》
                ああいう ﾛｰﾏ(aaiu)
                that sort of 《person》; 《a man》 like that; such 《people》.
                """),
            dedent(u"""\
                うきふね【浮舟】 ﾛｰﾏ(ukifune)
                relief; embossed carving.
                ▲浮き彫りの　＝<LINK>〜にした</LINK[113004:190]>
                2 〔際立たせる〕 throw sth into relief.
                ▲今回の騒動でその党内の不和が図らずも浮き彫りにされた.　In the latest upheaval, the political party's internal discord was inadvertently exposed.
                ああいう ﾛｰﾏ(aaiu)
                that sort of 《person》; 《a man》 like that; such 《people》.
                """),
            dedent(u"""\
                うきふね【浮舟】 ﾛｰﾏ(ukifune)
                relief; embossed carving.
                ▲浮き彫りの　＝<LINK>〜にした</LINK[113004:190]>
                2 〔際立たせる〕 throw sth into relief.
                ▲今回の騒動でその党内の不和が図らずも浮き彫りにされた.　In the latest upheaval, the political party's internal discord was inadvertently exposed.
                ああいう ﾛｰﾏ(aaiu)
                that sort of 《person》; 《a man》 like that; such 《people》.
                """),
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

        for multi_entry in test_multi_entries:
            print multi_entry
            parsed_entries = c.parse_multiple_entries(multi_entry)
            print c.get_json(parsed_entries)
            print
                

if __name__ == '__main__':
    unittest.main()
