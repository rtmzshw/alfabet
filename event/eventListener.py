from event.eventSchema import EventSchema
from sqlalchemy.event import listen
from event.subscription.subscriptionDal import get_subscriptions_by_event

def _on_event_change(_, __, target):
    subscriptions = get_subscriptions_by_event(target.id)
    if(not subscriptions):
        pass
    for sub in subscriptions:
        print(f"need to notify user {sub.user_id} that event {target.id} changed")

def register_event_table_listeners():
    listen(EventSchema, 'after_update', _on_event_change)
