from bs4 import BeautifulSoup
import requests
import re

class Scrape:

    def check_blog(self):
        page_to_scrape = requests.get("https://pokemongolive.com/news?hl=en")
        soup = BeautifulSoup(page_to_scrape.content, "html.parser")
        first_anchor = soup.find("a", class_="blogList__post")
        with open('latest_event.txt') as file:
            stored_event = file.readline()
            if stored_event != ("https://pokemongolive.com" + first_anchor['href']):
                with open('latest_event.txt', 'w') as file:
                    file.truncate(0)
                    file.write("https://pokemongolive.com" + first_anchor['href'])
                    self.add_event(first_anchor)
                    file.close
            else:
                print("Recorded events are up to date!")

    def get_event_date(self, first_anchor):
        page_to_scrape = requests.get("https://pokemongolive.com" + first_anchor['href'])
        soup = BeautifulSoup(page_to_scrape.content, "html.parser")
        container_divs = soup.find_all("div", class_="ContainerBlock__body")
        day = re.compile(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", re.IGNORECASE)
        for container_div in container_divs:
            p_tags = container_div.find_all("p")
            for p_tag in p_tags:
                p_text = p_tag.get_text()
                if day.search(p_text):
                    print(p_text)
                    break


    def add_event(self, first_anchor):
        page_to_scrape = requests.get("https://pokemongolive.com" + first_anchor['href'])
        soup = BeautifulSoup(page_to_scrape.content, "html.parser")
        container_divs = soup.find_all("div", class_="ContainerBlock__body")
        day = re.compile(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", re.IGNORECASE)
        for container_div in container_divs:
            p_tags = container_div.find_all("p")
            for p_tag in p_tags:
                p_text = p_tag.get_text()
                if day.search(p_text):
                    print(p_text)
                    break
