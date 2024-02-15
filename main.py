import requests
import selectorlib
from emaling import send_email
import sqlite3
import time


connection = sqlite3.Connection("data.db")
URL = "https://programmer100.pythonanywhere.com/tours/"

def scrape(url):
    response = requests.get(URL)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return  value

# def send_email():
#     print("email was sent!")


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)",row)
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band = ? AND city = ? AND date = ?",(band,city,date))
    rows = cursor.fetchall()

    return rows




if __name__ == "__main__":
    while True:

        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:

                store(extracted=extracted)
                send_email(extracted)
        time.sleep(2)





