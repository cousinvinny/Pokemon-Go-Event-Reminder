from bs4 import BeautifulSoup
import requests
import re

page_to_scrape = requests.get("https://pokemongolive.com/post/dark-flames-2023?hl=en")
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