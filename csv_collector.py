from bs4 import BeautifulSoup
import requests
import re
from csv import writer
import datetime


def get_csv_now():
    req = requests.get("https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-300/c37l1700273")
    max_page_finder = re.findall("page-([0-9]+)/", str(req.url))
    max_number_pagination = int(max_page_finder[0])
    # print(int(max_page[0]))

    def collect_data(page_number):
        url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-" + str(page_number) + "/c37l1700273"

        page = requests.get(url, allow_redirects=False)

        soup = BeautifulSoup(page.content, 'html.parser')

        cards = soup.find_all("div", class_=re.compile("search-item"))

        now = datetime.datetime.now()
        for card in cards:
            try:
                image = card.find(re.compile("img"))["data-src"]
            except KeyError:
                image = None
                continue
            title = card.find("a", class_="title").text.replace('\n', '').strip()
            date_posted = card.find("span", class_="date-posted").text.replace('\n', '').strip()
            location = card.find("div", class_="location").text.replace('\n', '').strip()
            bedrooms = card.find("span", class_="bedrooms").text.replace('\n', '').strip()
            description = card.find("div", class_="description").text.replace('\n', '').strip()
            price = card.find("div", class_="price").text.replace('\n', '').strip()

            image_clear = ' '.join(image.split())
            title_clear = ' '.join(title.split())
            date_posted_clear = ' '.join(date_posted.split())
            location_clear = ' '.join(location.split())
            bedrooms_clear = ' '.join(bedrooms.split())
            description_clear = ' '.join(description.split())
            price_clear = ' '.join(price.split())

            info_cleaned = [image_clear, title_clear, date_posted_clear, location_clear,
                                bedrooms_clear, description_clear, price_clear]
            # print(info_cleaned)
            thewriter.writerow(info_cleaned)

    pagination = 0
    now = datetime.datetime.now()
    with open("rs_data_" + str(now.strftime("%d-%m-%Y_%H-%M-%S")) + ".csv", "w", encoding="utf8", newline="") as f:
        thewriter = writer(f, delimiter =';')
        header = ["image_url", "title", "date_posted", "location", "bedrooms", "description", "price"]
        thewriter.writerow(header)

        for pagination in range(max_number_pagination):
            try:
                # pagination += 1
                collect_data(pagination)
                print("NOW PAGE IS_ ", pagination, " out of ", max_number_pagination, "___ to csv")
            except KeyError as kerr:
                print(kerr)
                continue
            except Exception as ex:
                print(ex)
                print("probably last page:", pagination)
                break # exit `while` loop
