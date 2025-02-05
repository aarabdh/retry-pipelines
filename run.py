import requests
import sys
import time
from datetime import datetime


GITLAB_URL = "PASTE_URL_HERE"
# Personal Access Token should have 'api' permission, otherwise it will not retry the pipeline.
PERSONAL_ACCESS_TOKEN = "PASTE_ACCESS_TOKEN_HERE"
PROJECT_ID = "PASTE_PROJECT_ID_HERE"

# Number of seconds the program will wait before pinging gitlab again. I recommend you keep this high to not overload your gitlab instance.
WAIT_BEFORE_EVERY_CHECK_SECONDS = 300

# Number of times this program will retry a failed pipeline before exiting
MAX_RETRY_COUNT = 5

#### Below code need not be modified before it is run ####

headers = {"PRIVATE-TOKEN": PERSONAL_ACCESS_TOKEN}
retry_count = 0

def get_pipeline_details(pipeline_id):
    url = "https://" + GITLAB_URL.replace('https://', '') + f"/api/v4/projects/{str(PROJECT_ID)}/pipelines/{str(pipeline_id)}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        printWithTime(f"get_pipeline_details Error: {response.status_code} - {response.text}")
        return None

def retry_pipeline(pipeline_id):
    url = "https://" + GITLAB_URL.replace('https://', '') + f"/api/v4/projects/{str(PROJECT_ID)}/pipelines/{str(pipeline_id)}/retry"
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        printWithTime("Pipeline retried successfully.")
        return
    else:
        printWithTime(f"retry_pipeline Error: {response.status_code} - {response.text}")
        return

def get_next_step(status):
    if status == "success":
        return 1
    elif status == "running":
        return 0
    else:
        return -1

def handle_success():
    print("Pipeline ran successfully.")

def handle_failure(pipeline_id):
    global retry_count
    printWithTime("Pipeline is in failure state.")
    if retry_count >= MAX_RETRY_COUNT:
        printWithTime("Pipeline failed after retrying 10 times")
        exit()
    retry_count += 1
    retry_pipeline(pipeline_id)
    ...

def getCurrentTime():
    return str(datetime.now())

def printWithTime(string):
    print(f"{getCurrentTime()} - {string}")

def run_pipeline(pipeline_id):
    print(f"Trying to get this pipeline green: {pipeline_id}")
    print("Press ctrl+c to stop the program.")
    try:
        while True:
            details = get_pipeline_details(pipeline_id)
            if not details:
                printWithTime("Couldn't get details from API.")
                exit()
            next = get_next_step(details["status"])
            if next == 0:
                time.sleep(WAIT_BEFORE_EVERY_CHECK_SECONDS)
                continue
            elif next == 1:
                handle_success()
                break
            else:
                handle_failure(pipeline_id)
    except KeyboardInterrupt:
        print("Ending the program before pipeline was successful.")
        exit(0)


if __name__ == "__main__":
    if PERSONAL_ACCESS_TOKEN == "ACCESS_TOKEN":
        print("Please modify the script with your Personal Access Token")
    if GITLAB_URL == "PASTE_URL_HERE":
        print("Please modify the script with your Gitlab URL.")
    if PROJECT_ID == "PASTE_PROJECT_ID_HERE":
        print("Please modify the script with your Project ID.")
    if len(sys.argv) != 2:
        print("Usage: python run.py <pipeline_id>")
        sys.exit(1)
    pipeline_id = sys.argv[1]
    pipeline_id = pipeline_id.replace("#", "")
    run_pipeline(pipeline_id)
