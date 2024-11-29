### **README.md**

```markdown
# SimilarWeb Scraper

This Python tool enables you to scrape traffic, geography, and demographic data from the SimilarWeb platform. It leverages Selenium for browser automation and provides structured, reusable methods for data extraction.

---

## Features

### 1. Traffic Data Extraction
- Monthly visits.
- Bounce rate.
- Pages per visit.
- Average visit duration.

### 2. Geography Data Extraction
- Percentage of traffic from different countries.

### 3. Demographics Data Extraction
- Gender distribution (male/female percentages).
- Age group distribution.

---

## Installation

### Prerequisites

1. **Python 3.7+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/).
2. **Firefox Browser**: Required for Selenium automation.
3. **GeckoDriver**:
   - Download [GeckoDriver](https://github.com/mozilla/geckodriver/releases) and add it to your system's PATH.

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/similarweb-scraper.git
   cd similarweb-scraper
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Example Script

Use the example script `example_usage.py` to scrape data for a specific domain:

1. Modify the `domain` variable in `example_usage.py` to the target website:
   ```python
   domain = "example.com"
   ```

2. Run the script:
   ```bash
   python example_usage.py
   ```

### Output

The script will print extracted data in the console, such as:
```plaintext
Scraping data for example.com...

Traffic Data:
{
    "monthly_visits": "1.2M",
    "bounce_rate": "45.3%",
    "pages_per_visit": "4.2",
    "visit_duration": "3m 15s"
}

Geography Data:
{
    "United States": "45.5%",
    "India": "10.2%",
    "United Kingdom": "8.1%"
}

Demographics Data:
{
    "Gender": {"Male": "55%", "Female": "45%"},
    "Age": {"18-24": "15%", "25-34": "30%", "35-44": "25%", "45-54": "20%", "55-64": "7%", "65+": "3%"}
}
```

---

## Code Structure

### `src/similarweb_scraper.py`

This file contains the main `SimilarWebScraper` class with the following methods:

1. **`scrape_traffic_data(domain)`**  
   Extracts traffic-related metrics.

2. **`scrape_geography_data(domain)`**  
   Collects traffic percentages by country.

3. **`scrape_demographics_data(domain)`**  
   Fetches demographic distributions by gender and age.

4. **`close()`**  
   Closes the Selenium WebDriver instance.

---

## Dependencies

The following Python libraries are required:

- `selenium==4.12.0`
- `beautifulsoup4==4.12.2`
- `requests==2.31.0`

Install them using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

## Notes

1. **Headless Mode**: The scraper runs in headless mode by default. To see browser interactions, modify the `SimilarWebScraper` initialization:
   ```python
   scraper = SimilarWebScraper(headless=False)
   ```

2. **Legal Considerations**: Ensure compliance with SimilarWeb's terms of service when using this scraper.
```