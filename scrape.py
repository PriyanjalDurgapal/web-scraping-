import requests
from bs4 import BeautifulSoup

def scrape_events():
    url = "https://concreteplayground.com/sydney/events"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    titles = []
    dates = []
    places = []
    image_urls = []
    ticket_urls = []
    event_ids = []  

   
    title_elements = soup.find_all("h2", class_="name title")
    for i, h2 in enumerate(title_elements):
        a_tag = h2.find("a")
        if a_tag:
            title_text = a_tag.text.strip()
            ticket_url = a_tag.get("href")
            titles.append(title_text)
            ticket_urls.append(ticket_url)
            event_ids.append(i)  

   
    date_elements = soup.find_all("p", class_="dates")
    for d in date_elements:
        date = d.text.strip()
        dates.append(date)

    
    place_elements = soup.find_all("p", class_="nearestPlace")
    for p in place_elements:
        place = p.text.strip()
        places.append(place)

    
    event_blocks = soup.find_all("div", class_="thumbnail")
    for block in event_blocks:
        img_tag = block.find("img", src=True)
        if img_tag:
            image_url = img_tag['src']
            image_urls.append(image_url)


    events = []
    for i in range(min(len(titles), len(dates), len(places), len(image_urls), len(ticket_urls), len(event_ids))):
        event = {
            "id": event_ids[i], 
            "Title": titles[i],
            "Date": dates[i],
            "Place": places[i],
            "Image": image_urls[i],
            "Book Ticket": ticket_urls[i]
        }
        events.append(event)

    return events
