#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import japanese_parser
import json
from sqlalchemy.sql import and_
import orm

def insert(conn, orm_class, **kwargs):
    new = True
    inserter = orm_class.__table__.insert().prefix_with('OR IGNORE')
    r = conn.execute(inserter.values(**kwargs))
    id_ = r.inserted_primary_key[0]
    if r.rowcount == 0:
        new = False
        filter_args = [orm_class.__table__.c[f]==kwargs[f] 
                       for f in orm_class.unique_fields]
        s = orm_class.__table__.select(and_(*filter_args))
        row = conn.execute(s).fetchone()
        id_ = row.id
    return (id_, new)

def insert_many(conn, orm_class, tuples):
    inserter = orm_class.__table__.insert().prefix_with('OR IGNORE')
    conn.execute(inserter, tuples)

def insert_many_core(conn, core_class, tuples):
    inserter = core_class.insert().prefix_with('OR IGNORE')
    conn.execute(inserter, tuples)

def read_entry(dict_file):
    fh = codecs.open(dict_file, 'r', 'utf-8')
    entry_buffer = list()
    for line in fh:
        if line == '\n':
            entry_lines = ''.join(entry_buffer)
            entry = json.loads(entry_lines)
            entry_buffer = list()
            yield entry
        else:
            entry_buffer.append(line)
    fh.close()

def insert_expression(conn, ue_expression, morpheme_cache, parser):
    expression_id, new_expression = insert(conn, orm.Expression, 
                                           expression=ue_expression)
    if new_expression:
        results = parser.parse(ue_expression)
        morphemes_in_expression = set() # items are (morpheme, type_id)

        # For bulk inserting the morpheme-expression association tuples
        expression_components = list()  # list of dicts representing fields

        for m in results.components:
            # Insert or get morpheme, (morpheme, type_id) unique
            morpheme_key = (m['base'], m['type'])
            if morpheme_key in morpheme_cache:
                morpheme_id = morpheme_cache[morpheme_key]
            else:
                morpheme_id = insert(conn, orm.Morpheme, 
                    morpheme=m['base'], type_id=m['type'])[0]
                morpheme_cache[morpheme_key] = morpheme_id
            print 'morpheme id:', morpheme_id

            morphemes_in_expression.add(morpheme_key)

            # Bulk insert later
            expression_components.append({'expression_id':expression_id, 
                                          'morpheme_id':morpheme_id, 
                                          'position':m['position'], 
                                          'word_length':m['length']})

        # Bulk insert the morpheme-expression association tuples
        if len(expression_components) > 0:
            insert_many(conn, orm.ExpressionConsistsOf, 
                        expression_components)

    return expression_id

def import_dictionary(dict_file):
    parser = japanese_parser.JapaneseParser()

    conn = orm.engine.connect()
    trans = conn.begin()

    lib_name = 'WADAI5'
    lib_id =  insert(conn, orm.Library, 
                     name=lib_name, type_id=orm.lib_type_dictionary.id)[0]

    # To reduce morpheme lookups
    morpheme_cache = dict() # (morpheme-unicode, type_id) -> morpheme-id

    for entry in read_entry(dict_file):
        print entry

        entry_header = entry['header']
        meanings = entry['meanings']

        kana = entry_header['kana']
        kanji_list = entry_header.get('kanji', list())
        entry_num = entry_header.get('number', 1)
        print "NUMBER!", entry_num

        kana_id = insert(conn, orm.Morpheme, morpheme=kana, 
                         type_id=orm.morpheme_types_ids['KANA_ENTRY'])[0]

        entry_id = insert(conn, orm.Entry, number=entry_num, library_id=lib_id, kana_id=kana_id)[0]

        entry_kanji = list()
        for kanji in kanji_list:
            kanji_id = insert(conn, orm.Morpheme, morpheme=kanji, 
                              type_id=orm.morpheme_types_ids['KANJI_ENTRY'])[0]
            entry_kanji.append({'entry_id':entry_id, 'kanji_id':kanji_id})

        insert_many_core(conn, orm.entry_has_kanji, entry_kanji)

        for meaning in meanings:
            meaning_text = meaning['dict_meaning']
            meaning_id = insert(conn, orm.Meaning, meaning=meaning_text, 
                                entry_id=entry_id)[0]
            usage_examples = meaning.get('usage_examples', list())
            meaning_ues = list()
            for ue in usage_examples:
                is_sentence = 1
                if 'sentence' in ue:
                    ue_expression = ue['sentence']['expression']
                    ue_meaning = ue['sentence']['meaning']
                elif 'phrase' in ue:
                    ue_expression = ue['phrase']['expression']
                    ue_meaning = ue['phrase'].get('meaning', None)
                    is_sentence = 0

                expression_id = insert_expression(conn, ue_expression, 
                                                  morpheme_cache, parser)

                usage_example_id = insert(conn, orm.UsageExample, 
                    expression_id=expression_id, library_id=lib_id, 
                    meaning=ue_meaning, is_sentence=is_sentence)[0]
                meaning_ues.append({'usage_example_id':usage_example_id, 
                                    'meaning_id':meaning_id})

            insert_many_core(conn, orm.meaning_has_ues, meaning_ues)


    trans.commit()
    conn.close()

def main():
    import_dictionary('kenconvert_small.txt')

if __name__ == '__main__':
    main()