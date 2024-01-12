from event.subscription.subscriptionSchema import SubscriptionSchema
from postgrese import engine
from sqlalchemy.orm import sessionmaker

from notification.notificationLogic import calc_notification_timing
from event.eventConfig import default_query_radius


def get_subscriptions_by_event(event_id: str):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        subscription = session.query(SubscriptionSchema).filter_by(
            event_id=event_id).all()
        return subscription


def toggle_subscription(user_id: str, event_id: str):
    Session = sessionmaker(bind=engine)
    status: str
    with Session() as session:
        subscription = session.query(SubscriptionSchema).filter_by(
            event_id=event_id, user_id=user_id).first()
        if subscription:
            session.query(SubscriptionSchema).filter_by(
                id=subscription.id).delete()
            status = "unsubscribed"
        else:
            suscription = SubscriptionSchema(
                event_id=event_id, user_id=user_id)
            session.add(suscription)
            status = "subscribed"

        session.commit()
        return status
