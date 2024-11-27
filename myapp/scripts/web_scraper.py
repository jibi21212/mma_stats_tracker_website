import string
from bs4 import BeautifulSoup
import requests
import sys
import os
import re
from datetime import datetime

# Add the root directory of your project to the Python path
sys.path.append("C:\\Users\\jibkh\\UFC\\UFC_PROJECT_WEBSITE")

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UFC_WEBSITE.settings')
import django
django.setup()

# Import your models after setting up Django
from myapp.models import Fighter, FighterStats, Bout

# Function to extract specific fighter data based on the label
def extract_fighter_data(fighter_soup, label):
    data = fighter_soup.find('i', string=lambda text: text and label in text)
    if data:
        parent_li = data.find_parent('li')
        if parent_li:
            value = parent_li.get_text(strip=True).replace(f'{label}', '').strip()
            return value
    return 'N/A'

# Function to convert height from feet and inches to centimeters
def convert_height(value):
    if value == 'N/A' or not value:
        return None
    match = re.match(r"(\d+)' (\d+)", value)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2))
        cm = round((feet * 30.48) + (inches * 2.54), 2)
        return cm
    print(f"Error converting height: {value}")
    return None

# Function to extract numerical value from percentage or other similar strings
def extract_percentage(value):
    if value == 'N/A' or not value:
        return None
    match = re.search(r'\d+(\.\d+)?', value)
    if match:
        return round(float(match.group(0)), 2)
    print(f"Error converting value: {value}")
    return None

# Function to convert weight or reach to float
def convert_to_float(value):
    try:
        return float(value.replace(' lbs', '').replace(' kg', '').replace(' cm', ''))
    except ValueError:
        return None
# Function to save bout data
def save_bout_to_db(fighter_1, fighter_2, method, result, winner_name, date):
    try:
        # Get fighters from the database
        fighter_1_obj = Fighter.objects.get(name=fighter_1)
        fighter_2_obj = Fighter.objects.get(name=fighter_2)

        # Determine the winner object or None for a draw
        winner = Fighter.objects.get(name=winner_name) if winner_name else None

        # Check if bout already exists
        existing_bout = Bout.objects.filter(fighter_1=fighter_1_obj, fighter_2=fighter_2_obj, date=date).exists()
        if existing_bout:
            print(f"Bout between {fighter_1} and {fighter_2} on {date} already exists. Skipping.")
            return

        # Create the bout entry
        bout = Bout(
            fighter_1=fighter_1_obj,
            fighter_2=fighter_2_obj,
            method=method,
            result=result,
            winner=winner,
            date=date
        )
        bout.save()
        print(f"Bout saved: {fighter_1} vs {fighter_2} on {date}")

    except Fighter.DoesNotExist as e:
        print(f"Error: {e}. Cannot save bout between {fighter_1} and {fighter_2}.")
# Updated save_fighter_to_db function
def save_fighter_to_db(name, wins, losses, draws, height, weight, reach, stance, dob):
    # Function to extract only numerical values from strings
    def extract_number(value):
        match = re.search(r'\d+', value)
        return int(match.group(0)) if match else 0

    # Convert DOB to the correct format if it's not 'N/A'
    if dob != 'N/A':
        try:
            dob = datetime.strptime(dob, "%b %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            print(f"Error parsing date of birth for {name}: {dob}")
            dob = None
    else:
        dob = None

    # Convert height properly
    height = convert_height(height)

    # Extract only numerical values from wins, losses, draws
    wins = extract_number(wins) if wins != 'N/A' else 0
    losses = extract_number(losses) if losses != 'N/A' else 0
    draws = extract_number(draws) if draws != 'N/A' else 0

    # Convert weight and reach to float if possible
    weight = convert_to_float(weight)
    reach = convert_to_float(reach)

    # Create or update a Fighter instance
    fighter, created = Fighter.objects.get_or_create(
        name=name,
        defaults={
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'height': height,
            'weight': weight,
            'reach': reach,
            'stance': stance,
            'dob': dob
        }
    )

    if created:
        print(f"New fighter created: {name}")
    else:
        print(f"Existing fighter found: {name}.")
        print(f"Existing data - Wins: {fighter.wins}, Losses: {fighter.losses}, Draws: {fighter.draws}, Height: {fighter.height}, Weight: {fighter.weight}, Reach: {fighter.reach}, DOB: {fighter.dob}, Stance: {fighter.stance}")
        print(f"New data - Wins: {wins}, Losses: {losses}, Draws: {draws}, Height: {height}, Weight: {weight}, Reach: {reach}, DOB: {dob}, Stance: {stance}")

    # Update existing fighter if they already exist, conditionally updating fields
    if not created:
        if wins is not None and fighter.wins != wins:
            print(f"Updating wins for {name} from {fighter.wins} to {wins}")
            fighter.wins = wins
        if losses is not None and fighter.losses != losses:
            print(f"Updating losses for {name} from {fighter.losses} to {losses}")
            fighter.losses = losses
        if draws is not None and fighter.draws != draws:
            print(f"Updating draws for {name} from {fighter.draws} to {draws}")
            fighter.draws = draws
        if height is not None and fighter.height != height:
            print(f"Updating height for {name} from {fighter.height} to {height}")
            fighter.height = height
        if weight is not None and fighter.weight != weight:
            print(f"Updating weight for {name} from {fighter.weight} to {weight}")
            fighter.weight = weight
        if reach is not None and fighter.reach != reach:
            print(f"Updating reach for {name} from {fighter.reach} to {reach}")
            fighter.reach = reach
        if stance is not None and fighter.stance != stance:
            print(f"Updating stance for {name} from {fighter.stance} to {stance}")
            fighter.stance = stance
        if dob is not None and fighter.dob != dob:
            print(f"Updating date of birth for {name} from {fighter.dob} to {dob}")
            fighter.dob = dob

        if any([wins != fighter.wins, losses != fighter.losses, draws != fighter.draws, height != fighter.height, weight != fighter.weight, reach != fighter.reach, stance != fighter.stance, dob != fighter.dob]):
            print(f"Saving updated data for: {name}")
            fighter.save()
            print(f"Data saved successfully for: {name}")

    return fighter

# Updated save_fighter_stats function
def save_fighter_stats(fighter, slpm, str_acc, sapm, str_def, td_avg, td_acc, td_def, sub_avg):
    # Convert stats to None if they are 'N/A'
    slpm = extract_percentage(slpm)
    str_acc = extract_percentage(str_acc)
    sapm = extract_percentage(sapm)
    str_def = extract_percentage(str_def)
    td_avg = extract_percentage(td_avg)
    td_acc = extract_percentage(td_acc)
    td_def = extract_percentage(td_def)
    sub_avg = extract_percentage(sub_avg)

    # Create or update a FighterStats instance for the given fighter
    print(f"Saving statistics for fighter: {fighter.name}")
    print(f"Advanced stats - SLpM: {slpm}, Str. Acc.: {str_acc}, SApM: {sapm}, Str. Def.: {str_def}, TD Avg.: {td_avg}, TD Acc.: {td_acc}, TD Def.: {td_def}, Sub. Avg.: {sub_avg}")
    stats, created = FighterStats.objects.get_or_create(
        fighter=fighter,
        defaults={
            'sig_strikes_perMin': slpm,
            'strikes_accuracy': str_acc,
            'sig_strikes_abs': sapm,
            'strike_def': str_def,
            'takedown_average_per15': td_avg,
            'takedowns_accuracy': td_acc,
            'takedown_defense': td_def,
            'sub_avg': sub_avg
        }
    )

    # Update stats if they already exist
    if not created:
        stats.sig_strikes_perMin = slpm
        stats.strikes_accuracy = str_acc
        stats.sig_strikes_abs = sapm
        stats.strike_def = str_def
        stats.takedown_average_per15 = td_avg
        stats.takedowns_accuracy = td_acc
        stats.takedown_defense = td_def
        stats.sub_avg = sub_avg
        stats.save()

def parse_date(date_text):
    try:
        if len(date_text.split()) == 3:
            return datetime.strptime(date_text, "%b %d, %Y").strftime("%Y-%m-%d")
        else:
            raise ValueError(f"Invalid date format: {date_text}")
    except ValueError:
        print(f"Error parsing date: {date_text}")
        return None


# Example of how to extract fighters' names correctly from bout details
def scrape_bout_details(fighter, opponent_name, result, method, date_text):
    # Parse date properly with validation
    date = parse_date(date_text)
    if not date:
        return  # Skip if the date couldn't be parsed

    try:
        opponent = Fighter.objects.get(name=opponent_name)
    except Fighter.DoesNotExist:
        print(f"Error: Fighter matching query does not exist. Cannot save bout between {fighter.name} and {opponent_name}.")
        return

    # Prevent duplicate bout entries
    bout, created = Bout.objects.get_or_create(
        fighter_1=fighter,
        fighter_2=opponent,
        defaults={
            'method': method,
            'result': result,
            'date': date,
        }
    )
    if created:
        print(f"Bout saved between {fighter.name} and {opponent.name}.")
    else:
        print(f"Bout already exists between {fighter.name} and {opponent.name}.")


# Function to scrape fighter profile
def scrape_fighter_profile(fighter_url):
    print(f"Accessing profile page: {fighter_url}")
    fighter_response = requests.get(fighter_url)

    if fighter_response.status_code != 200:
        print(f"Failed to access {fighter_url}, status code: {fighter_response.status_code}")
        return

    fighter_soup = BeautifulSoup(fighter_response.content, 'html.parser')

    # Scraping fighter's name
    name_element = fighter_soup.select_one('span.b-content__title-highlight')

    if name_element:
        name = name_element.get_text(strip=True)
    else:
        print(f"Name not found at {fighter_url}. Skipping...")
        return  # Skip if no name is found

    # Scrape fighter's height, weight, reach, stance, and DOB
    record = fighter_soup.select_one('span.b-content__title-record')
    if record:
        record_text = record.get_text(strip=True)
        record_values = record_text.replace("Record:", "").strip()
        wins, losses, draws = record_values.split('-')
    else:
        wins = losses = draws = 'N/A'

    height = extract_fighter_data(fighter_soup, "Height:")
    weight = extract_fighter_data(fighter_soup, "Weight:")
    reach = extract_fighter_data(fighter_soup, "Reach:")
    stance = extract_fighter_data(fighter_soup, "STANCE:")
    dob = extract_fighter_data(fighter_soup, "DOB:")

    # Save fighter basic details to the database
    fighter = save_fighter_to_db(name, wins, losses, draws, height, weight, reach, stance, dob)

    # Extract bout history and save it
    bout_history = fighter_soup.select('.b-fight-details__table-row')

    for bout in bout_history:
        columns = bout.select('td')

        if len(columns) >= 5:
            opponent_name = columns[1].get_text(strip=True)
            result = columns[2].get_text(strip=True)
            method = columns[3].get_text(strip=True)
            date_text = columns[4].get_text(strip=True)

            # Convert the date to the correct format
            try:
                date = datetime.strptime(date_text, "%b %d, %Y").strftime("%Y-%m-%d")
            except ValueError:
                print(f"Error parsing date: {date_text}")
                continue

            # Save the bout to the database
            scrape_bout_details(fighter, opponent_name, result, method, date)

# Keep track of already scraped fighter URLs to avoid duplication
visited_fighter_urls = set()

# Loop through each letter of the alphabet and scrape fighter profiles
for alphabet in string.ascii_lowercase:
    url = f"http://www.ufcstats.com/statistics/fighters?char={alphabet}&page=all"
    print(f"Accessing fighters list page: {url}")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to access {url}, status code: {response.status_code}")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all fighter names and links
    fighters = soup.find_all('a', class_='b-link b-link_style_black')

    if not fighters:
        print(f"No fighters found for letter: {alphabet.upper()}")
        continue

    print(f"Fighters whose last name starts with {alphabet.upper()}:")
    
    # Loop through each fighter
    for fighter in fighters:
        fighter_name = fighter.get_text().strip()
        fighter_url = fighter['href']  # Extract the fighter's personal page link

        # Check if this URL has already been visited
        if fighter_url in visited_fighter_urls:
            continue  # Skip duplicates

        # Add the URL to the visited set
        visited_fighter_urls.add(fighter_url)

        # Ensure we're accessing a new fighter profile each time
        print(f"Accessing profile page for {fighter_name}: {fighter_url}")
        scrape_fighter_profile(fighter_url)

    print("-" * 40)  # Separator between letters
