# Google Search Enrichment App

The Google Search Enrichment App is a web application that allows users to perform Google searches, scrape LinkedIn profiles, and enrich data from the search results.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Features

- Perform Google searches with specified parameters (location, language, number of results, search term).
- Scrape LinkedIn profiles from the search results.
- Enrich scraped data with additional LinkedIn profile information.
- Download enriched data as a CSV file.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- The `serpapi` library installed. You can install it using `pip`:

pip install serpapi

- The Selenium WebDriver installed, if you plan to use the LinkedIn profile enrichment feature. Download and install the appropriate WebDriver for your browser (e.g., ChromeDriver).


## Usage

1. Run the Flask application:

python app.py

2. Access the web application in your browser at `http://127.0.0.1:5000`.

3. Enter the search parameters (location, language, number of results, search term) and click the "Search" button.

4. After the search results are displayed, you can click the "Enrich" button to perform LinkedIn profile enrichment (requires Selenium WebDriver).

5. Download the enriched data as a CSV file by clicking the provided download link.

## Customization

You can customize the web application by modifying the HTML templates, CSS styles, and JavaScript code in the project files. Adjust the design, layout, and behavior to meet your specific requirements.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the project repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b bugfix/issue-number`.
3. Commit your changes and push them to your fork: `git push origin feature/your-feature-name`.
4. Create a pull request (PR) to the main repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
