from requests import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium .webdriver.chrome.options import Options

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
base_url = "https://kr.indeed.com/jobs"
browser = webdriver.Chrome(options=options)


def get_page_count(keyword):
    final_url = f'{base_url}?q={keyword}'
    browser.get(final_url)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", class_="ecydgvn0")
    if pagination == None:
        return 1
    pages = pagination.find_all("div", recursive=False)
    count = len(pages) - 1
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):
        final_url = f'{base_url}?q={keyword}'
        browser.get(final_url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all('li', recursive=False)
        # while (True):
        #     pass
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                # h2 = job.find("h2", class_="jobTitle")
                anchor = job.select_one("h2 a")
                # if anchor != None:
                title = anchor["aria-label"]
                link = anchor["href"]
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    "link": f"https://kr.indeed.com{link}",
                    "company": company.string.replace(",", " "),
                    "location": location.string.replace(",", " "),
                    "position": title.replace(",", " ")
                }
                results.append(job_data)

    return results


# print(extract_indeed_jobs("node"))
