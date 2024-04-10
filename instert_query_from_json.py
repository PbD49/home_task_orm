from models import Publisher, Shop, Book, Stock, Sale
import json


def populate_db(session):
    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)

        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
            session.commit()
