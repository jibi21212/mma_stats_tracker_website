from prefect import task, Flow
from prefect import IntervalSchedule
import subprocess
from datetime import timedelta

# Define the schedule to run every 6 hours, for example
schedule = IntervalSchedule(interval=timedelta(hours=100000))

@task
def update_ufc_database():
    # Call db_update.py using subprocess
    subprocess.run(['python', 'myapp/scripts/db_update.py'], check=True)

with Flow("UFC Database Update", schedule=schedule) as flow:
    update_ufc_database()

# Execute the flow (optional for testing)
if __name__ == "__main__":
    flow.run()
