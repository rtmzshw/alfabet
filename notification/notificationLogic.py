from datetime import datetime, timedelta
from utils import set_interval
from notification.notificationSchema import NotificationSchema
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
from postgrese import engine
from datetime import datetime
from notification.notificationConfig import notification_offset_in_minutes, notification_poller_in_seconds

""" Not the optimal solution, but chosen due to time constraints.
    In a real-world scenario, I would consider one of the following alternatives:
    1- A service with scheduling capabilities (e.g., like Airflow): 
       When a notification is created, schedule a task to handle it.
    2- Delayed message queue: Although less optimal, it can still fulfill the requirement.
       Send a message with a delay to the specified date.
"""


def calc_notification_timing(date: datetime):
    modified_date = date - timedelta(minutes=notification_offset_in_minutes)
    return modified_date.strftime("%Y-%m-%d %H:%M:%S")


def notify():
    notifications = get_notifications()
    for notification in notifications:
        description = notification[0]
        print("notifying:", description)


def get_notifications():
    now = datetime.now()
    table = NotificationSchema.__table__
    Session = sessionmaker(bind=engine)
    with Session() as session:
        update_statement = table.update().returning(NotificationSchema.description) \
            .where(NotificationSchema.date <= now) \
            .where(NotificationSchema.sent == False) \
            .values(sent=True)

        result = session.execute(update_statement)
        notifications = result.fetchall()
        session.commit()
        return notifications


def register_notifications():
    set_interval(notify, notification_poller_in_seconds)
