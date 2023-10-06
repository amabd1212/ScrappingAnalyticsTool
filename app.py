from flask import Flask, request, jsonify, render_template, send_file
import json
from serpapi import GoogleSearch
import csv
import os  # Add this import
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


app = Flask(__name__, template_folder='/Users/tnwuser/Documents/TNW/TNW/static')

app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()

    location = data.get("location", "World")
    language = data.get("language", "en")
    number = data.get("number", 10)
    search_for = data.get("subject","")
    search_term = data.get("search_term", "")

    with open("locations.json", "r") as json_file:
        country_data_list = json.load(json_file)

    domain = 0
    for country_data in country_data_list:
        if country_data["country_name"] == location:
            domain = country_data['domain']
            break

    if domain == 0:
        domain = "google.com"


    with open("google-countries.json", "r") as json_file:
        country_data_list = json.load(json_file)

    country = 0
    for country_data in country_data_list:
        if country_data["country_name"] == location:
            country = country_data['domain']
            break

    if country == 0:
        country = "nl"


    with open("languages.json", "r") as json_file:
        languages_data_list = json.load(json_file)

    language_code = 0
    for language_data in languages_data_list:
        if language_data["language_name"] == language:
            language_code = language_data['language_code']
            break

    if language_code == 0:
        language_code = "en"

    params = {
        "api_key": "f3d6b2422082d454c234957bbdf93152469256fecb0937efc6e0fb975d7acb4a",
        "engine": "google",
        "q": f"site:linkedin.com/in/ {search_term} AND {search_for}",
        "google_domain": domain,
        "gl": country,
        "hl": language_code,
        "safe": "off",
        "num": number,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    csv_file_path = 'output.csv'

    # Save the results to a JSON file
    with open("google_search_results.json", "w") as json_file:
        json.dump(results, json_file, indent=2)
        
    with open("google_search_results.json", "r") as json_file:
        data = json.load(json_file)

    # Extract and save only the "organic_results"
    organic_results = data.get("organic_results", [])

    # Create a new JSON file with only the "organic_results"
    with open("organic_results.json", "w") as organic_file:
        json.dump(organic_results, organic_file, indent=2)

    # Load the JSON data
    with open('organic_results.json', 'r') as json_file:
        data = json.load(json_file)

    # Create a CSV file for writing
    with open('output.csv', 'w', newline='') as csv_file:
        # Define the CSV writer and write the header row
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['title', 'link'])

        # Loop through the JSON data and write each title and link as a row in the CSV file
        for item in data:
            title = item.get('title', '')
            link = item.get('link', '')
            csv_writer.writerow([title, link])

    # Return the path of the generated CSV file
    return jsonify({'csv_path': csv_file_path})

@app.route('/download_csv', methods=['GET'])  # Add a new route for downloading the CSV
def download_csv():
    # Specify the path to the CSV file on your server
    csv_file_path = 'output.csv'

    # Check if the file exists
    if os.path.exists(csv_file_path):
        return send_file(csv_file_path, as_attachment=True, download_name='output.csv')
    else:
        return "CSV file not found", 404
    
@app.route('/enrich', methods=['POST'])
def enrich_data():
    # Initialize the Selenium WebDriver (make sure you have the WebDriver installed and in your PATH)
    driver = webdriver.Chrome()

    # Login to LinkedIn
    driver.get('https://www.linkedin.com/login')
    time.sleep(5)
    username = driver.find_element(By.ID, 'username')
    password = driver.find_element(By.ID, 'password')
    username.send_keys('amir.aziz@thenextweb.com')  # Replace with your LinkedIn username
    password.send_keys('TestAI2023')  # Replace with your LinkedIn password
    driver.find_element(By.XPATH, '//button[text()="Sign in"]').click()

    # Read LinkedIn profile data from a CSV file
    profile_data = []
    with open('output.csv', 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            profile_data.append(row)

    # Create a CSV file to store the scraped data
    with open('enriched_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Title', 'Profile Description', 'Current Job Title'])

        for data in profile_data:
            title = data['title']
            linkedin_link = data['link']

            try:
                # Open the LinkedIn profile URL using Selenium
                driver.get(linkedin_link)

                # Wait for the page to load (you may need to adjust the waiting time)
                time.sleep(10)

                # Extract the profile description using CSS selector
                profile_description_elements = driver.find_element(By.CSS_SELECTOR,'.text-body-medium.break-words')
                profile_description = profile_description_elements.text if profile_description_elements else ""


                # Extract the current job title using CSS selector
                current_job_element = driver.find_element(By.CSS_SELECTOR, '.display-flex.flex-column.full-width.align-self-center')
                current_job_title = current_job_element.text if current_job_element else ""

                # Extract the 1st and 3rd lines from the entire string
                if current_job_title:
                    job_title_lines = current_job_title.split('\n')
                    if len(job_title_lines) >= 3:
                        job_title = job_title_lines[0]
                        duration = job_title_lines[2]
                        current_job_title = f"{job_title}\n{duration}"
                    else:
                        current_job_title = ""


                # Write the data to the CSV file
                csv_writer.writerow([title, profile_description, current_job_title])
            except Exception as e:
                print(f"Error scraping LinkedIn profile: {str(e)}")

    # Close the Selenium WebDriver
    driver.quit()
    enriched_data_link = 'enriched_data.csv'  # Replace with the actual path
    return enriched_data_link

if __name__ == '__main__':
    app.run()
