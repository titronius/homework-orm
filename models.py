import sqlalchemy as sq
import json
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=120), unique=True)

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=120))
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=120), unique=True)

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sales")

def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def data_add(session):
    with open('test_data/test_data.json', 'r') as fd:
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

def get_sales(session,publisher_data):
    #My var
    # q = session.query(Sale).join(Sale.stock).join(Stock.book).join(Stock.shop).join(Book.publisher)
    # if publisher_data.isdigit():
    #     res = q.filter(Publisher.id == publisher_data).all()
    # else:
    #     res = q.filter(Publisher.name == publisher_data).all()
    # text = ""
    # if res:
    #     text = "название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки"
    # for s in res:
    #     text += f"\n{s.stock.book.title} | {s.stock.shop.name} | {s.price}  |  {s.date_sale}"
    # return text
    #My var
    
    #Teacher var
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale,).\
        select_from(Shop).\
        join(Stock).\
        join(Book).\
        join(Publisher).\
        join(Sale)
    if publisher_data.isdigit():
        res = q.filter(Publisher.id == publisher_data).all()
    else:
        res = q.filter(Publisher.name == publisher_data).all()
    text = ""
    if res:
        text = "название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки"
        for book_title, shop_name, sale_price, sale_data in res:
            text += f"\n{book_title: <40} | {shop_name: <10} | {sale_price: <8} | {sale_data.strftime('%d-%m-%Y')}"
    return text
    #Teacher var