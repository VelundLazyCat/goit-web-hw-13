from sqlalchemy import Column, Integer, String, func, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Author(Base):
    __tablename__ = "quotes_author"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(), nullable=False)
    born_date = Column(String(), nullable=False)
    born_location = Column(String(), nullable=False)
    description = Column(String(), nullable=False)


class Quote(Base):
    __tablename__ = "quotes_quote"
    id = Column(Integer, primary_key=True)
    quote = Column(String(), nullable=False)
    author_id = Column('author_id', ForeignKey(
        'quotes_author.id', ondelete='CASCADE'), nullable=False)


class Tag(Base):
    __tablename__ = "quotes_tag"
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)


class QuoteTags(Base):
    __tablename__ = "quotes_quote_tags"
    id = Column(Integer, primary_key=True)
    quote_id = Column('quote_id', ForeignKey(
        'quotes_quote.id', ondelete='CASCADE'), nullable=False)
    tag_id = Column('tag_id', ForeignKey(
        'quotes_tag.id', ondelete='CASCADE'), nullable=False)
