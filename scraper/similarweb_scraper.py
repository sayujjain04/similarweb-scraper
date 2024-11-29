import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json

def setup_selenium():
    options = Options()
    # Uncomment the line below to run headless (without opening the browser window)
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    return driver

def generate_similarweb_url(domain, section="#traffic"):
    return f"https://www.similarweb.com/website/{domain}/{section}"

def wait_for_element(driver, selector, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element with selector: {selector}")
        return None

def scrape_traffic_data(driver, url):
    driver.get(url)
    if not wait_for_element(driver, "div.engagement-list"):
        return {}

    traffic_data = {}
    try:
        monthly_visits = driver.find_element(By.CSS_SELECTOR, "div.engagement-list:nth-child(1) > div:nth-child(1) > p:nth-child(2)").text
        bounce_rate = driver.find_element(By.CSS_SELECTOR, "div.engagement-list:nth-child(1) > div:nth-child(3) > p:nth-child(2)").text
        pages_per_visit = driver.find_element(By.CSS_SELECTOR, "div.engagement-list:nth-child(1) > div:nth-child(4) > p:nth-child(2)").text
        visit_duration = driver.find_element(By.CSS_SELECTOR, "div.engagement-list__item:nth-child(5) > p:nth-child(2)").text

        traffic_data['monthly_visits'] = monthly_visits
        traffic_data['bounce_rate'] = bounce_rate
        traffic_data['pages_per_visit'] = pages_per_visit
        traffic_data['visit_duration'] = visit_duration

        print(f"Scraped traffic data: {traffic_data}")

    except NoSuchElementException as e:
        print(f"Error finding traffic data on page: {e}")

    return traffic_data

def scrape_geography_data(driver, url):
    driver.get(url)
    if not wait_for_element(driver, "div.wa-geography__country-info"):
        return {}

    demographics = {}
    try:
        demographic_blocks = driver.find_elements(By.CSS_SELECTOR, "div.wa-geography__country-info")
        for block in demographic_blocks:
            try:
                country_name = block.find_element(By.CSS_SELECTOR, ".wa-geography__country-name").text
                traffic_percentage = block.find_element(By.CSS_SELECTOR, ".wa-geography__country-traffic-value").text
                demographics[country_name] = traffic_percentage
            except NoSuchElementException:
                print(f"Error finding demographic data in block: {block}")

        print(f"Scraped geography data: {demographics}")

    except NoSuchElementException as e:
        print(f"Error finding geography data on page: {e}")

    return demographics

def scrape_demographics_data(driver, url):
    driver.get(url)
    if not wait_for_element(driver, "li.wa-demographics__gender-legend-item"):
        return {}

    time.sleep(1)
    demographics_data = {}
    try:
        male_percentage = driver.find_element(By.CSS_SELECTOR, "li.wa-demographics__gender-legend-item:nth-child(2) > span:nth-child(2)").text
        female_percentage = driver.find_element(By.CSS_SELECTOR, "li.wa-demographics__gender-legend-item:nth-child(1) > span:nth-child(2)").text

        demographics_data['GenderDemographics'] = {
            'male_percentage': male_percentage,
            'female_percentage': female_percentage
        }

        age_groups = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
        age_data = {}
        age_elements = driver.find_elements(By.CSS_SELECTOR, ".wa-demographics__age-data-label")
        for i, age_element in enumerate(age_elements):
            if i < len(age_groups):
                age_percentage = age_element.text
                age_data[age_groups[i]] = age_percentage

        demographics_data['AgeDemographics'] = age_data

        print(f"Scraped gender demographics: {demographics_data['GenderDemographics']}")
        print(f"Scraped age demographics: {demographics_data['AgeDemographics']}")

    except NoSuchElementException as e:
        print(f"Error finding demographics data on page: {e}")

    return demographics_data

def scrape_traffic_sources_data(driver, url):
    driver.get(url)
    time.sleep(0.5)

    traffic_sources_data = {}
    try:
        traffic_sources = ["Direct", "Referrals", "Organic Search", "Paid Search", "Social", "Mail", "Display"]
        source_elements = driver.find_elements(By.CSS_SELECTOR, ".wa-traffic-sources__channels-data-label")
        for i, source_element in enumerate(source_elements):
            if i < len(traffic_sources):
                source_percentage = source_element.text
                traffic_sources_data[traffic_sources[i]] = source_percentage

        print(f"Scraped traffic sources data: {traffic_sources_data}")

    except NoSuchElementException as e:
        print(f"Error finding traffic sources data on page: {e}")

    return traffic_sources_data

def scrape_keywords_data(driver, url):
    driver.get(url)
    top_keywords_data = {}

    try:
        keyword_elements = driver.find_elements(By.CSS_SELECTOR, ".wa-vectors-list__item.wa-vectors-list__item--md")
        for element in keyword_elements:
            try:
                keyword_title = element.find_element(By.CSS_SELECTOR, ".wa-vectors-list__item-title").text
                keyword_value = element.find_element(By.CSS_SELECTOR, ".wa-vectors-list__item-value").text
                keyword_volume = element.find_element(By.CSS_SELECTOR, ".wa-vectors-list__item-subtitle").text.replace("VOL: ", "")
                keyword_cpc = element.find_element(By.CSS_SELECTOR, ".wa-vectors-list__item-sub-value").text
                top_keywords_data[keyword_title] = [keyword_value, keyword_volume, keyword_cpc]

            except NoSuchElementException:
                print(f"Error extracting data from keyword element: {element}")

        print(f"Scraped top keywords data: {top_keywords_data}")

    except NoSuchElementException as e:
        print(f"Error finding keywords data on page: {e}")

    return top_keywords_data

def scrape_social_media_data(driver, url):
    driver.get(url)
    time.sleep(1)

    social_media_data = {}
    try:
        total_social_traffic = driver.find_element(By.CSS_SELECTOR, ".app-parameters__item-value").text
        social_media_data['TotalSocialNetworks'] = total_social_traffic

        social_media_platforms = []
        platform_elements = driver.find_elements(By.CSS_SELECTOR, ".wa-social-media__chart-label-title")
        for element in platform_elements:
            platform_name = element.text
            social_media_platforms.append(platform_name)

        traffic_elements = driver.find_elements(By.CSS_SELECTOR, ".wa-social-media__chart-data-label")
        traffic_percentages = [element.text for element in traffic_elements]

        social_media_distribution = {}
        for i, platform in enumerate(social_media_platforms):
            if i < len(traffic_percentages):
                social_media_distribution[platform] = traffic_percentages[i]

        social_media_data['SocialMediaTraffic'] = social_media_distribution

        print(f"Scraped social media data: {social_media_data}")

    except NoSuchElementException as e:
        print(f"Error finding social media data on page: {e}")

    return social_media_data

def save_results_to_json(domain, data, json_path):
    try:
        with open(json_path, 'r') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    existing_data[domain] = data

    with open(json_path, 'w') as file:
        json.dump(existing_data, file, indent=4)
    print(f"Data saved to {json_path}")

# SEO and Accessibility Functions
def fetch_page(url):
    try:
        start_time = time.time()
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        load_time = time.time() - start_time
        response.raise_for_status()
        return response.text, load_time
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, 0

def parse_seo_metrics(html, base_url):
    soup = BeautifulSoup(html, 'lxml')
    seo_data = {}

    seo_data['title'] = soup.title.string if soup.title else 'No Title Found'

    description = soup.find('meta', attrs={'name': 'description'})
    seo_data['meta_description'] = description['content'] if description else 'No Meta Description Found'

    heading_tags = {f'h{i}': [] for i in range(1, 7)}
    for i in range(1, 7):
        tags = soup.find_all(f'h{i}')
        heading_tags[f'h{i}'] = [tag.get_text(strip=True) for tag in tags]
    seo_data['headings'] = heading_tags

    viewport = soup.find('meta', attrs={'name': 'viewport'})
    seo_data['mobile_friendly'] = bool(viewport)

    internal_links = set()
    external_links = set()
    broken_links = set()
    anchor_texts = []
    parsed_base_url = urlparse(base_url)

    for link in soup.find_all('a', href=True):
        href = link.get('href')
        anchor_texts.append(link.get_text(strip=True))
        full_url = urljoin(base_url, href)
        parsed_href = urlparse(full_url)

        if parsed_href.netloc == parsed_base_url.netloc:
            internal_links.add(full_url)
        else:
            external_links.add(full_url)

        try:
            link_response = requests.head(full_url, timeout=5)
            if link_response.status_code >= 400:
                broken_links.add(full_url)
        except requests.RequestException:
            broken_links.add(full_url)

    seo_data['internal_links'] = list(internal_links)
    seo_data['external_links'] = list(external_links)
    seo_data['total_links'] = len(internal_links) + len(external_links)
    seo_data['broken_links'] = list(broken_links)
    seo_data['anchor_texts'] = anchor_texts

    text = soup.get_text()
    seo_data['total_word_count'] = len(text.split())

    images = soup.find_all('img')
    images_without_alt = [img['src'] for img in images if not img.get('alt')]
    seo_data['total_images'] = len(images)
    seo_data['images_without_alt'] = images_without_alt

    canonical_link = soup.find('link', rel='canonical')
    seo_data['canonical'] = canonical_link['href'] if canonical_link else 'No Canonical Tag Found'

    structured_data = soup.find_all('script', type='application/ld+json')
    seo_data['structured_data_present'] = bool(structured_data)

    seo_data['accessibility'] = check_accessibility(soup)

    return seo_data

def check_accessibility(soup):
    accessibility_data = {}

    aria_roles = [tag.get('role') for tag in soup.find_all(attrs={"role": True})]
    accessibility_data['aria_roles'] = aria_roles if aria_roles else 'No ARIA Roles Found'

    forms_missing_labels = []
    for form in soup.find_all('form'):
        inputs = form.find_all(['input', 'textarea', 'select'])
        for inp in inputs:
            if not inp.get('aria-label') and not inp.find_previous_sibling('label'):
                forms_missing_labels.append(str(inp))

    accessibility_data['forms_missing_labels'] = len(forms_missing_labels)

    skip_links = [link.get('href') for link in soup.find_all('a', href=True) if 'skip' in link.get('href', '').lower()]
    accessibility_data['skip_navigation_links'] = skip_links if skip_links else 'No Skip Navigation Links Found'

    missing_tabindex = [tag.name for tag in soup.find_all(['a', 'button', 'input']) if tag.get('tabindex') is None]
    accessibility_data['missing_tabindex'] = missing_tabindex if missing_tabindex else 'All Elements Accessible via Keyboard'

    contrast_issues = []
    for tag in soup.find_all(style=True):
        style = tag['style'].lower()
        if 'color' in style and 'background' in style and '#ffffff' not in style:
            contrast_issues.append(tag.name)

    accessibility_data['contrast_issues'] = contrast_issues if contrast_issues else 'No Contrast Issues Found'

    return accessibility_data

def crawl_website(url, max_pages=5):
    visited_links = set()
    to_visit_links = set([url])
    all_internal_links = set()
    seo_reports = []

    while to_visit_links and len(visited_links) < max_pages:
        current_url = to_visit_links.pop()
        if current_url in visited_links:
            continue

        print(f"Crawling: {current_url}")
        html, load_time = fetch_page(current_url)
        if not html:
            continue

        seo_metrics = parse_seo_metrics(html, current_url)
        seo_reports.append(seo_metrics)

        for link in seo_metrics['internal_links']:
            if link not in visited_links:
                to_visit_links.add(link)
                all_internal_links.add(link)

        visited_links.add(current_url)

    print("\n=== List of All Discovered Internal Links ===")
    for link in sorted(all_internal_links):
        print(link)

    return seo_reports

def main():
    domains = ['hiutdenim.co.uk', 'example.com']
    json_path = 'WebData.json'

    driver = setup_selenium()

    for domain in domains:
        traffic_url = generate_similarweb_url(domain, "#traffic")
        print(f"Scraping traffic data for: {traffic_url}")
        traffic_data = scrape_traffic_data(driver, traffic_url)

        geography_url = generate_similarweb_url(domain, "#geography")
        print(f"Scraping geography data for: {geography_url}")
        geography_data = scrape_geography_data(driver, geography_url)

        demographics_url = generate_similarweb_url(domain, "#demographics")
        print(f"Scraping demographics data for: {demographics_url}")
        demographics_data = scrape_demographics_data(driver, demographics_url)

        traffic_sources_url = generate_similarweb_url(domain, "#traffic-sources")
        print(f"Scraping traffic sources data for: {traffic_sources_url}")
        traffic_sources_data = scrape_traffic_sources_data(driver, traffic_sources_url)

        keywords_url = generate_similarweb_url(domain, "#keywords")
        print(f"Scraping keywords data for: {keywords_url}")
        keywords_data = scrape_keywords_data(driver, keywords_url)

        social_media_url = generate_similarweb_url(domain, "#social-media")
        print(f"Scraping social media data for: {social_media_url}")
        social_media_data = scrape_social_media_data(driver, social_media_url)

        seo_reports = crawl_website(f"https://{domain}", max_pages=5)

        combined_data = {
            "TrafficData": traffic_data,
            "NationalityDemographics": geography_data,
            "Demographics": demographics_data,
            "TrafficSources": traffic_sources_data,
            "TopKeyWords": keywords_data,
            "SocialMediaTraffic": social_media_data,
            "SEOReports": seo_reports
        }

        save_results_to_json(domain, combined_data, json_path)

    driver.quit()

if __name__ == "__main__":
    main()  