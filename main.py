import sqlalchemy
from sqlalchemy.orm import sessionmaker
from instert_query_from_json import populate_db
from models import create_tables, Publisher, Shop, Book, Stock, Sale
import configparser


config = configparser.ConfigParser()
config.read("settings.ini")
username = config["name"]["username"]
password = config["password"]["password"]


DSN = f'postgresql://{username}:{password}@localhost:5432/shop_db'
engine = sqlalchemy.create_engine(DSN)


Session = sessionmaker(bind=engine)
session = Session()


create_tables(engine)

populate_db(session)


select_query = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
                .join(Stock, Book.id == Stock.id_book)
                .join(Shop, Stock.id_shop == Shop.id)
                .join(Sale, Stock.id == Sale.id_stock)
                .join(Publisher, Book.id_publisher == Publisher.id))


input_data = input('Введите имя или ID для поиска данных: ')


if input_data.isdigit():
    result = select_query.filter(Publisher.id == input_data)
else:
    result = select_query.filter(Publisher.name == input_data)


for book, shop, price, date in select_query:
    print(f"{book: <40} | {shop: <10} | {price: <8} | {date.strftime('%d-%m-%Y')}")
