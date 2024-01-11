from datetime import date as datetime

class Notification:
    id = int
    description = str
    date = datetime
    creation_date = datetime    
    event_id = str
    sent: bool