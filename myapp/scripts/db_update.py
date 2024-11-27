from prefect import flow, task
import os
import sys

# Adding your project's root directory to the Python path
sys.path.append(os.path.abspath("C:\\Users\\jibkh\\UFC\\UFC_PROJECT_WEBSITE"))

# Import the web scraper script
from web_scraper import scrape_fighter_profile


@task
def scrape_data_task():
    # You can adapt the main scraping loop from your web_scraper here
    from string import ascii_lowercase
    from bs4 import BeautifulSoup
    import requests

    # Keep track of already scraped fighter URLs to avoid duplication
    visited_fighter_urls = set()

    # Loop through each letter of the alphabet and scrape fighter profiles
    for alphabet in ascii_lowercase:
        url = f"http://www.ufcstats.com/statistics/fighters?char={alphabet}&page=all"
        print(f"Accessing fighters list page: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to access {url}, status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        fighters = soup.find_all('a', class_='b-link b-link_style_black')

        if not fighters:
            print(f"No fighters found for letter: {alphabet.upper()}")
            continue

        # Loop through each fighter and scrape their profiles
        for fighter in fighters:
            fighter_name = fighter.get_text().strip()
            fighter_url = fighter['href']

            if fighter_url in visited_fighter_urls:
                continue

            visited_fighter_urls.add(fighter_url)
            print(f"Accessing profile page for {fighter_name}: {fighter_url}")
            scrape_fighter_profile(fighter_url)

@flow
def update_database_flow():
    scrape_data_task()

if __name__ == "__main__":
    update_database_flow()
