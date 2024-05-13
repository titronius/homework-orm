import sqlalchemy
from sqlalchemy.orm import sessionmaker
import settings
from models import create_tables, data_add, get_sales

DSN = settings.DSN
engine = sqlalchemy.create_engine(DSN)

if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()

    create_tables(engine)
    data_add(session)

    publisher_data = None
    while publisher_data != '0':
        publisher_data = input('Введите ID или имя издателя или 0 для выхода: ')
        res = get_sales(session,publisher_data)
        print(res)