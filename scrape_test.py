from scrape import Scrape
from event import Event

scr = Scrape()
event = Event()
scr.check_blog()
with open('latest_event.txt') as file:
    stored_event = file.readline()
    file.close()
date = scr.scrape_event_date()
print(date)
event = scr.parse_event_date(date)
event.summary = scr.scrape_event_title()
print(event.start_day)
