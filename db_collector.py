import psycopg2
from bs4 import BeautifulSoup
import requests
import re

def get_db_now():
    hostname = 'localhost'
    database = '' #enter your database
    username = 'postgres'
    pwd = '' #enter your password
    port_id = 5432

    conn = None
    cur = None

    req = requests.get("https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-300/c37l1700273")
    max_page_finder = re.findall("page-([0-9]+)/", str(req.url))
    max_number_pagination = int(max_page_finder[0]) # get last page of site

    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id
        )

        cur = conn.cursor()

        create_script = ''' DROP TABLE IF EXISTS collected_data;
                            CREATE TABLE IF NOT EXISTS collected_data (
                                id  SERIAL,
                                image_url    varchar(250),
                                title   varchar(400),
                                date_posted varchar(150),
                                location varchar(200),
                                bedrooms varchar(150),
                                description varchar(500),
                                price varchar(150)
                                );'''
        cur.execute(create_script)

        insert_script = '''INSERT INTO collected_data (image_url, title,
                                                    date_posted, location, bedrooms,
                                                    description, price)
                        VALUES(%s, %s, %s, %s, %s, %s, %s);
                        '''

        def collect_data(page_number):
            url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-" + str(page_number) + "/c37l1700273"

            page = requests.get(url, allow_redirects=False)

            soup = BeautifulSoup(page.content, 'html.parser')

            cards = soup.find_all("div", class_=re.compile("search-item"))

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

                info_cleaned = (image_clear, title_clear, date_posted_clear, location_clear,
                                bedrooms_clear, description_clear, price_clear)
                insert_value = info_cleaned
                cur.execute(insert_script, insert_value)
                conn.commit()



        for pagination in range(max_number_pagination):
                collect_data(pagination)
                print("NOW PAGE IS_ ", pagination, " out of ", max_number_pagination, "___ to pgsql db")

        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if cur or conn is not None:
            cur.close()
            conn.close()