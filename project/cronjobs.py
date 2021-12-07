import time
import atexit

from cs50 import SQL
from apscheduler.schedulers.background import BackgroundScheduler

from minibuses import minibuses_data

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


def store_minibuses_data():
    # Get minibus information from API

    result = minibuses_data()

    # Start Insert to db
    db.execute("BEGIN TRANSACTION")
    for obj in result:
        sql = f"INSERT INTO minibuses(route_id,district,route_name,company_code,start_name,end_name,url,duration,price,route_seq) VALUES (?,?,?,?,?,?,?,?,?,?) ON CONFLICT(route_id, route_seq) DO UPDATE SET district = excluded.district, route_name = excluded.route_name, company_code = excluded.company_code, start_name = excluded.start_name, end_name = excluded.end_name, duration = excluded.duration, url = excluded.url, price = excluded.price;"
        db.execute(sql, obj["route_id"], obj["district"], obj["route_name"], obj["company_code"],
                   obj["start_name"], obj["end_name"], obj["url"], obj["duration"], obj["price"], obj["route_seq"])
    db.execute("END TRANSACTION")
    print("Cron Job Finish")


# Register CronJob
def cron():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=store_minibuses_data, trigger="interval", minutes=60)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


# Run Application
if __name__ == "__main__":
    store_minibuses_data()

