from scrape import Scrape

scr = Scrape()

with open('latest_event.txt') as file:
    stored_event = file.readline()

scr.get_event_date(stored_event)
