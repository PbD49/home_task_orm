from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    book = relationship('Book', back_populates='publisher')


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(40), unique=True)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)
    publisher = relationship('Publisher', back_populates='book')
    stock = relationship('Stock', back_populates='book')


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    book = relationship('Book', back_populates='stock')
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    shop = relationship('Shop', back_populates='stock')
    sale = relationship('Sale', back_populates='stock')
    count = Column(Integer, nullable=False)


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date_sale = Column(String(40), nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    stock = relationship('Stock', back_populates='sale')
    count = Column(Integer, nullable=False)


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    stock = relationship('Stock', back_populates='shop')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
