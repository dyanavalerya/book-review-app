import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://kspasxxpngjmqc:f7ddbb2d6ba9b1d81d836730cd15010ed35f80e6302cdf133c85c2876d296cf6@ec2-54-217-204-34.eu-west-1.compute.amazonaws.com:5432/d198utkr325v5v")
db = scoped_session(sessionmaker(bind=engine))

def table():
    db.execute("""CREATE TABLE imported_books ( isbn VARCHAR NOT NULL PRIMARY KEY, title VARCHAR NOT NULL, author VARCHAR NOT NULL,
    year VARCHAR NOT NULL);""")

def main():
    table()
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO imported_books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn":isbn, "title": title, "author": author, "year": year})
        print(f"Added book with {isbn} isbn to the database.")
    db.commit()

if __name__ == "__main__":
    main()
