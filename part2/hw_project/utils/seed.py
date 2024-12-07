import json

from my_db import session
from models import Author, Quote, Tag, QuoteTags

with open('utils/authors.json', 'r', encoding='utf=8') as file:
    data_authors = json.load(file)

with open('utils/quotes.json', 'r', encoding='utf=8') as file:
    data_quotes = json.load(file)


def seed_authors():
    for item in data_authors:
        author = Author(
            fullname=item['fullname'],
            born_date=item['born_date'],
            born_location=item['born_location'],
            description=item['description']
        )
        session.add(author)
    session.commit()


def seed_quotes():
    for item in data_quotes:
        value = item['author']
        query = session.query(Author.id).filter_by(fullname=value)
        author_id = query.scalar()
        quote = Quote(quote=item['quote'],
                      author_id=author_id)
        session.add(quote)
    session.commit()


def seed_tags():
    for item in data_quotes:
        for tag in item['tags']:
            query = session.query(Tag).filter(Tag.name == tag)
            exists = session.query(query.exists()).scalar()
            if not exists:
                tag_ps = Tag(
                    name=tag,
                )
                session.add(tag_ps)
    session.commit()


def seed_quote_tags():
    for item in data_quotes:
        query = session.query(Quote.id).filter_by(quote=item["quote"])
        repr(query)
        quote_id = query.first()[0]
        for tag in item['tags']:
            query = session.query(Tag.id).filter_by(name=tag)
            tag_id = query.first()[0]
            quote_tag = QuoteTags(
                quote_id=quote_id,
                tag_id=tag_id
            )
            session.add(quote_tag)
    session.commit()


if __name__ == '__main__':
    ...
    # Розкоментувати ждя заповнення потрібної БД
    # seed_authors()
    # seed_quotes()
    # seed_tags()
    # seed_quote_tags()
