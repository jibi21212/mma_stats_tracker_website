from prefect import task, Flow
from myapp.scripts.web_scraper import scrape_ufc_data
from myapp.scripts.db_update import update_database  # Import database update logic (if needed)

@task
def scrape_data():
    # Call the scraping logic from `web_scraper.py`
    data = scrape_ufc_data()  # Assume scrape_ufc_data() returns the scraped data
    return data

@task
def update_db(data):
    # Update the database with scraped data
    update_database(data)

# Define the Prefect Flow
with Flow("UFC Scraper Flow") as flow:
    data = scrape_data()
    update_db(data)

if __name__ == "__main__":
    flow.run()
