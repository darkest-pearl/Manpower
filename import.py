import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://munira:trash@localhost:5432/flasky")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("insert.csv")
    reader = csv.reader(f)
    for origin, destination, duration in reader:
        db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
        {"origin": origin, "destination": destination, "duration": duration})

        print (f"Added flight from {origin} to {destination} lasting {duration} minutes")
    db.commit()

if __name__ == "__main__":
    main()