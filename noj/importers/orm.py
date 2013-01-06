#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker, relationship)
from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Table)
from sqlalchemy.schema import UniqueConstraint

# engine = create_engine('sqlite:///:memory:', echo=True)
# engine = create_engine('sqlite:///known_test.db', echo=True)
engine = create_engine('sqlite:///wadai5_small.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Library(Base):
    """Represents a Usage Example Library."""

    __tablename__ = 'libraries'

    id      = Column(Integer, primary_key=True)
    name    = Column(String, nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey('librarytypes.id'), nullable=False)

    lib_type = relationship('LibraryType', backref='libraries')

    unique_fields = ['name']

    def __repr__(self):
        return "<Library(%s)>" % (self.name)

class LibraryType(Base):
    """Represents a Usage Example Library Type"""

    __tablename__ = 'librarytypes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return "<LibraryType(%s)>" % (self.name)

entry_has_kanji = Table(
    'entryhaskanji', Base.metadata,
    Column('entry_id', Integer, ForeignKey('entries.id'), primary_key=True),
    Column('kanji_id', Integer, ForeignKey('morphemes.id'), primary_key=True))

class Entry(Base):
    """Represents a dictionary entry."""

    __tablename__ = 'entries'

    id         = Column(Integer, primary_key=True)
    number     = Column(Integer)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    kana_id    = Column(Integer, ForeignKey('morphemes.id'), nullable=False)

    library = relationship('Library', backref='entries')
    kana    = relationship('Morpheme', backref='entries_from_kana')
    kanji   = relationship('Morpheme', secondary=entry_has_kanji, backref='entries_from_kanji')

    unique_fields = []

    def __repr__(self):
        return "<Entry({!r}, {!r}, {!r}, {!r})>".format(self.kana, self.kanji, self.number, self.library)

meaning_has_ues = Table(
    'meaninghasues', Base.metadata,
    Column('usage_example_id', Integer, ForeignKey('usageexamples.id'), primary_key=True),
    Column('meaning_id', Integer, ForeignKey('meanings.id'), primary_key=True))

class Meaning(Base):
    """Represents a dictionary meaning."""

    __tablename__ = 'meanings'

    id       = Column(Integer, primary_key=True)
    meaning  = Column(String)
    entry_id = Column(Integer, ForeignKey('entries.id'), nullable=False)

    entry = relationship('Entry', backref='meanings')
    usage_examples  = relationship('UsageExample', secondary=meaning_has_ues, backref='meanings')

    def __repr__(self):
        return "<Meaning(%s)>" % (self.meaning)

class Expression(Base):
    """Represents a Japanese Expression."""

    __tablename__ = 'expressions'

    id         = Column(Integer, primary_key=True)
    expression = Column(String, nullable=False, unique=True)

    unique_fields = ['expression']

    def __repr__(self):
        return "<Expression({!r})>".format(self.expression)

class UsageExample(Base):
    """Represents a usage example."""

    __tablename__ = 'usageexamples'

    id            = Column(Integer, primary_key=True)
    expression_id = Column(Integer, ForeignKey('expressions.id'), nullable=False)
    library_id    = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    meaning       = Column(String)
    reading       = Column(String)
    is_sentence   = Column(Integer, nullable=False)

    expression = relationship('Expression', backref='usage_examples')
    library    = relationship('Library', backref='usage_examples')

    __table_args__ = (UniqueConstraint('library_id', 'expression_id', name='_library_expression_uc'),
                     )

    unique_fields = ['library_id', 'expression_id']

    def __repr__(self):
        return "<UsageExample({!r}, {!r})>".format(self.expression, self.meaning)


class MorphemeType(Base):
    """Represents a morpheme type"""

    __tablename__ = 'morphemetypes'

    id      = Column(Integer, primary_key=True)
    name    = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return "<MorphemeType({!r})>".format(self.name)

class Morpheme(Base):
    """Represents a morpheme"""

    __tablename__ = 'morphemes'

    id       = Column(Integer, primary_key=True)
    morpheme = Column(String, nullable=False)
    type_id  = Column(Integer, ForeignKey('morphemetypes.id'), nullable=False)
    count    = Column(Integer)

    morpheme_type = relationship('MorphemeType', backref='morphemes')

    unique_fields = ['morpheme', 'type_id']

    __table_args__ = (UniqueConstraint('morpheme', 'type_id', name='_morpheme_morpheme_type_uc'),
                     )

    def __repr__(self):
        return "<Morpheme({!r}, {!r}, {!r})>".format(self.morpheme, self.morpheme_type, self.count)

class ExpressionConsistsOf(Base):
    """Association object between expression and morphemes."""

    __tablename__ = 'expressionconsistsof'

    expression_id = Column(Integer, ForeignKey('expressions.id'), primary_key=True)
    morpheme_id   = Column(Integer, ForeignKey('morphemes.id'), primary_key=True)
    position      = Column(Integer, nullable=False, primary_key=True)
    word_length   = Column(Integer, nullable=False)

    expression = relationship('Expression', backref='morpheme_assocs')
    morpheme   = relationship('Morpheme', backref='expression_assocs')

    def __repr__(self):
        return "<ExpressionConsistsOf('{!r}, {!r}, {!r}, {!r}')>".format(self.morpheme, self.expression, self.position, self.word_length)

ue_part_of_list = Table(
    'uepartoflist', Base.metadata,
    Column('ue_list_id', Integer, ForeignKey('uelists.id'), primary_key=True),
    Column('usage_example_id', Integer, ForeignKey('usageexamples.id'), primary_key=True))

class UEList(Base):
    """Represents a list of usage examples"""

    __tablename__ = 'uelists'

    id      = Column(Integer, primary_key=True)
    name    = Column(String, nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey('uelisttypes.id'), nullable=False)

    list_type = relationship('UEListType', backref='lists')
    usage_examples  = relationship('UsageExample', secondary=ue_part_of_list, backref='ue_lists')

    def __repr__(self):
        return "<UEList('{!r}')>".format(self.name)

class UEListType(Base):
    """Represents a type of usage example list."""

    __tablename__ = 'uelisttypes'

    id      = Column(Integer, primary_key=True)
    name    = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return "<UEListType('{!r}')>".format(self.name)

def unescape(string):
    return unicode(str(string), 'unicode-escape')

def get_or_create(session, model, **kwargs):
    # http://stackoverflow.com/a/6078058/1030774
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance

def get_or_create_on(session, model, on=None, **kwargs):
    # http://stackoverflow.com/a/6078058/1030774
    if on is None:
        on = kwargs
    else:
        on = {key:kwargs[key] for key in on}
    instance = session.query(model).filter_by(**on).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance

Base.metadata.create_all(engine)
lib_type_dictionary = get_or_create(session, LibraryType, name='DICTIONARY')
lib_type_corpus     = get_or_create(session, LibraryType, name='CORPUS')
ue_list_type_user      = get_or_create(session, UEListType, name='USER')
ue_list_type_reviewing = get_or_create(session, UEListType, name='REVIEWING')
ue_list_type_staged    = get_or_create(session, UEListType, name='STAGED')
session.commit()

conn = engine.connect()
trans = conn.begin()

morpheme_types = ['INTERJECTION', 
                  'ADVERB', 
                  'PRE_NOUN_ADJECTIVAL', 
                  'NOUN', 
                  'AUXILIARY_VERB',
                  'VERB',
                  'PARTICLE',
                  'PREFIX',
                  'ADJECTIVE',
                  'CONJUNCTION',
                  'FILLER',
                  'SYMBOL',
                  'OTHER',
                  'KANJI_ENTRY',
                  'KANA_ENTRY']

morpheme_types_ids = dict([(type_, i+1) for i, type_ in enumerate(morpheme_types)])

conn.execute(MorphemeType.__table__.insert().prefix_with("OR IGNORE"),
    [{'id':id_, 'name':type_} for type_, id_ in morpheme_types_ids.items()])

trans.commit()
# conn.close()


def main():
    kenkyusha = Library(name='Kenkyusha')
    print kenkyusha        
    kenkyusha.lib_type = lib_type_dictionary
    session.add(kenkyusha)
    session.commit()

    print("stdout encoding=%s" % (sys.stdout.encoding))
    kana_type = session.query(MorphemeType).filter_by(name='KANA_ENTRY').one()
    kanji_type = session.query(MorphemeType).filter_by(name='KANJI_ENTRY').one()
    print kana_type
    test_kana = Morpheme(morpheme=u'せんせい', morpheme_type=kana_type)
    # print unicode(test_kana)
    # s1= u"<Morpheme({:s})>".format(test_kana.morpheme)
    # print s1
    print test_kana
    test_kanji = Morpheme(morpheme=u'先生', morpheme_type=kanji_type)
    session.add(test_kana)
    session.add(test_kanji)
    test_entry = Entry(library=kenkyusha, kana=test_kana, kanji=[test_kanji])
    print test_entry
    session.add(test_entry)

    session.commit()
    print unescape(test_entry)

    e1 = get_or_create(session, Expression, expression=u'納入した品の代金が未払いだ.')
    e2 = get_or_create(session, Expression, expression=u'納入した品の代金が未払いだ.')
    print unescape(e1), unescape(e2)
    session.add_all([e1, e2])
    session.commit()

if __name__ == '__main__':
    main()
