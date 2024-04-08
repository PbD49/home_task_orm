import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = f'postgresql://postgres:5814@localhost:5432/shop_db'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

publisher1 = Publisher(name='Пушкин')
publisher2 = Publisher(name='Лермонтов')
session.add(publisher1)
session.add(publisher2)

book1 = Book(title='Капитанская дочка', publisher=publisher1)
book2 = Book(title='Руслан и Людмила', publisher=publisher1)
book3 = Book(title='Евгений Онегин', publisher=publisher1)
session.add(book1)
session.add(book2)
session.add(book3)

shop1 = Shop(name='Буквоед')
shop2 = Shop(name='Лабиринт')
shop3 = Shop(name='Книжный дом')
session.add(shop1)
session.add(shop2)
session.add(shop3)

stock1 = Stock(book=book1, shop=shop1, count=600)
stock2 = Stock(book=book2, shop=shop1, count=500)
stock3 = Stock(book=book1, shop=shop2, count=580)
stock4 = Stock(book=book3, shop=shop3, count=490)
session.add(stock1)
session.add(stock2)
session.add(stock3)
session.add(stock4)

sale1 = Sale(price=600, date_sale='09-11-2022', stock=stock1, count=600)
sale2 = Sale(price=500, date_sale='08-11-2022', stock=stock2, count=500)
sale3 = Sale(price=580, date_sale='05-11-2022', stock=stock3, count=580)
sale4 = Sale(price=490, date_sale='02-11-2022', stock=stock4, count=490)
sale5 = Sale(price=600, date_sale='26-10-2022', stock=stock1, count=600)
session.add(sale1)
session.add(sale2)
session.add(sale3)
session.add(sale4)
session.add(sale5)

session.commit()

input_data = input('Введите имя или ID для поиска данных: ')

try:
    input_id = int(input_data)
    select_query = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
                    .join(Stock, Book.id == Stock.id_book)
                    .join(Shop, Stock.id_shop == Shop.id)
                    .join(Sale, Stock.id == Sale.id_stock)
                    .join(Publisher, Book.id_publisher == Publisher.id)
                    .filter(Publisher.id == input_id).all())
except ValueError:
    select_query = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
                    .join(Stock, Book.id == Stock.id_book)
                    .join(Shop, Stock.id_shop == Shop.id)
                    .join(Sale, Stock.id == Sale.id_stock)
                    .join(Publisher, Book.id_publisher == Publisher.id)
                    .filter(Publisher.name == input_data).all())

for results in select_query:
    print(results)
