"""Webscraper class that uses Pokemon GO news page"""

from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from event import Event

class Scrape:
    """Webscraper class that uses Pokemon GO news page"""

    def check_blog(self):
        """Checks if a new event was posted on the website and updates latest_event.txt if new event exists"""
        print("Checking if a new event exists...")
        page_to_scrape = requests.get("https://pokemongolive.com/news?hl=en",timeout=10)
        soup = BeautifulSoup(page_to_scrape.content, "html.parser")
        first_anchor = soup.find("a", class_="blogList__post")
        with open('latest_event.txt', encoding='UTF-8') as file:
            stored_event = file.readline()
            possible_new_event = "https://pokemongolive.com" + first_anchor['href']
            if stored_event != (possible_new_event):
                scr = Scrape()
                if scr.scrape_event_date_from_link(possible_new_event) is None:
                    print("New blog post is not an event!")
                else:
                    with open('latest_event.txt', 'w', encoding='UTF-8') as file:
                        print('New event found...')
                        file.truncate(0)
                        file.write(possible_new_event)
                        file.close()
                        print("Updated latest event link in file!")
            else:
                print("Recorded events are up to date!")

    def scrape_event_date(self):
        """Finds the container on the website that contains the event date using the link from the file"""
        with open('latest_event.txt', encoding='UTF-8') as file:
            event_link = file.readline()
            file.close()
        page_to_scrape = requests.get(event_link,timeout=10)
        soup = BeautifulSoup(page_to_scrape.content, "html.parser")
        container_divs = soup.find_all("div", class_="ContainerBlock__body")
        day = re.compile(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", re.IGNORECASE)
        for container_div in container_divs:
            p_tags = container_div.find_all("p")
            for p_tag in p_tags:
                p_text = p_tag.get_text()
                if day.search(p_text):
                    return p_text

    def scrape_event_date_from_link(self, possible_new_event):
        """Attempts to find a date from a new event blog post"""
        page_to_scrape = requests.get(possible_new_event, timeout=10)
        soup = BeautifulSoup(page_to_scrape.content, "html.parser")
        container_divs = soup.find_all("div", class_="ContainerBlock__body")
        day = re.compile(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", re.IGNORECASE)
        for container_div in container_divs:
            p_tags = container_div.find_all("p")
            for p_tag in p_tags:
                p_text = p_tag.get_text()
                if day.search(p_text):
                    return p_text

    def scrape_event_title(self):
        """Finds the event title on the event page"""
        with open('latest_event.txt', encoding='UTF-8') as file:
            event_link = file.readline()
            file.close()
        page_to_scrape = requests.get(event_link, timeout=10)
        soup = BeautifulSoup(page_to_scrape.content, "html.parser")
        span_element = soup.find("span", class_="ContainerBlock__headline__title")
        return span_element.get_text()

    def parse_event_date(self, string_date):
        """Breaks up the event date to store into Event object"""
        string_date = string_date.replace(","," ")
        string_date = string_date.replace("at","")
        string_date = string_date.replace("local time","")
        string_date = string_date.replace("to","")
        string_date = string_date.replace("  "," ").replace("  ", " ")
        string_date = string_date.rstrip()
        start_day, month1, day1, year1, start_time, amOrPm1, end_day, month2, day2, year2, end_time, amOrPm2 = string_date.split(" ")
        event = Event()
        event.start_day = start_day
        event.month1 = self.convert_month_to_num(month1)
        event.day1 = day1
        event.year1 = year1
        time_obj = start_time + " " + amOrPm1
        time_obj = time_obj.replace(".","")
        time_obj = datetime.strptime(time_obj, "%I:%M %p")
        military_time_str = time_obj.strftime("%H:%M")
        event.start_time = military_time_str
        event.end_day = end_day
        event.month2 = self.convert_month_to_num(month2)
        event.day2 = day2
        event.year2 = year2
        time_obj = end_time + " " + amOrPm2
        time_obj = time_obj.replace(".","")
        time_obj = datetime.strptime(time_obj, "%I:%M %p")
        military_time_str = time_obj.strftime("%H:%M")
        event.end_time = military_time_str
        return event

    def convert_month_to_num(self, month):
        """Helper function to convert date format"""
        if month == 'January':
            return '01'
        if month == 'February':
            return '02'
        if month == 'March':
            return '03'
        if month == 'April':
            return '04'
        if month == 'May':
            return '05'
        if month == 'June':
            return '06'
        if month == 'July':
            return '07'
        if month == 'August':
            return '08'
        if month == 'September':
            return '09'
        if month == 'October':
            return '10'
        if month == 'November':
            return '11'
        if month == 'December':
            return '12'
        