from event.eventSchema import EventSchema
from sqlalchemy.event import listen
from event.subscription.subscriptionDal import get_subscriptions_by_event

def _on_row_change(_, __, target):
    # TODO get all assosiated subs
    subscriptions = get_subscriptions_by_event(target.id)
    if(not subscriptions):
        pass
    for sub in subscriptions:
        print(f"need to notify user {sub.user_id} that event {target.id} changed")

def register_event_table_listeners():
    listen(EventSchema, 'before_update', _on_row_change)
