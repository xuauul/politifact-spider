import json

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import FirefoxOptions


class PolitifactNewsSpider:
    def __init__(self, category):
        self.category = category
        self.base_url = f"https://www.politifact.com/factchecks/list/?category={self.category}&page="
        self.page = 1

    def run(self):
        filename = f"data/politifact.json"

        with open(filename, 'w', encoding="utf-8") as fout:
            for data in self.get_data():
                fout.write(json.dumps(data, ensure_ascii=False) + '\n')

    def get_data(self):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        opts.add_argument("start-maximized")
        opts.add_argument("disable-infobars")
        opts.add_argument("--disable-extensions")
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-application-cache')
        opts.add_argument('--disable-gpu')
        opts.add_argument("--disable-dev-shm-usage")

        with webdriver.Firefox(options=opts) as driver:

            while True:
                print(f"Crawling Page {self.page} ...")
                driver.get(self.base_url + str(self.page))
                sleep(2)

                soup = BeautifulSoup(driver.page_source, "html.parser")
                for li in soup.select("li.o-listicle__item"):
                    # try to crawl one news data in a page
                    try:
                        data = {
                            "date": ' '.join(li.select(".m-statement__desc")[0].string.strip().split()[2:5]),
                            "label": li.select(".m-statement__meter .c-image__original")[0]["alt"],
                            "source": li.select(".m-statement__name")[0]["title"],
                            "text": li.select(".m-statement__content a")[0].string.strip(),
                            "verify_date": li.select("footer")[0].string.split('•')[1].strip(),
                            "verify_url": "https://politifact.com" + li.select(".m-statement__content a")[0]["href"],
                        }
                        yield data
                    except Exception as e:
                        print(e)
                
                # stop when the next page button does not exist
                if "Next" in [a.string.strip() for a in soup.select(".c-button")]:
                    self.page += 1
                else:
                    break

            driver.quit()


if __name__ == "__main__":
    spider = PolitifactNewsSpider(category="coronavirus")
    spider.run()
