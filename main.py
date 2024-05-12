import sqlalchemy
from sqlalchemy.orm import sessionmaker
import settings
from models import create_tables, Publisher, Book, Stock, Sale

DSN = settings.DSN
engine = sqlalchemy.create_engine(DSN)

if __name__ == "__main__":
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    publisher_id = None
    while publisher_id != '0':
        publisher_id = input('Введите ID издателя или 0 для выхода: ')
        q = session.query(Sale).join(Sale.stock).join(Stock.book).join(Stock.shop).join(Book.publisher).filter(Publisher.id == publisher_id)
        res = q.all()
        if res:
            print("название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки")
        for s in res:
            print(f"{s.stock.book.title} | {s.stock.shop.name} | {s.price}  |  {s.date_sale}")