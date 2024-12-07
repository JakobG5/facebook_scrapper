from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time
import csv
import re

# Load environment variables
load_dotenv()

class FacebookPageScraper:
    def __init__(self):
        # Updated Chrome initialization
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)
        self.min_followers = 10000
        self.results = []

    def login(self, email, password):
        try:
            print("Attempting to log in...")
            self.driver.get('https://www.facebook.com')
            
            # Wait for and enter email
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
            email_field.send_keys(email)
            
            # Enter password
            password_field = self.wait.until(EC.presence_of_element_located((By.ID, 'pass')))
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.wait.until(EC.element_to_be_clickable((By.NAME, 'login')))
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            print("Login successful!")
            return True
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False

    def search_ethiopian_pages(self, search_term):
        try:
            # Updated search URL format
            search_url = f'https://www.facebook.com/search/pages?q={search_term}'
            print(f"Accessing URL: {search_url}")
            self.driver.get(search_url)
            time.sleep(5)

            pages_found = []
            
            # Wait for page content to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"]')))
            
            # Scroll and collect results
            for _ in range(5):  # Scroll 5 times to load more results
                # Find all page links and titles
                page_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
                
                for elem in page_elements:
                    try:
                        # Get the link and name directly from the search results
                        link_elem = elem.find_element(By.CSS_SELECTOR, 'a')
                        page_url = link_elem.get_attribute('href')
                        page_name = link_elem.text
                        
                        if page_url and page_url not in [p['url'] for p in pages_found]:
                            pages_found.append({
                                'url': page_url,
                                'name': page_name
                            })
                            print(f"Found page: {page_name} ({page_url})")
                    except Exception as e:
                        continue

                # Scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

            print(f"Total pages found for '{search_term}': {len(pages_found)}")
            return pages_found
            
        except Exception as e:
            print(f"Search failed: {str(e)}")
            return []

    def analyze_page(self, page_data):
        try:
            page_url = page_data['url']
            print(f"\nAnalyzing page: {page_data['name']}")
            
            # Navigate to the page
            self.driver.get(page_url)
            time.sleep(3)
            
            def convert_to_number(text):
                """Convert text like '1.2K', '2.5M', '900K' to actual numbers"""
                try:
                    text = text.strip().lower()
                    if 'k' in text:
                        # Handle thousands (K)
                        number = float(text.replace('k', '').strip())
                        return int(number * 1000)
                    elif 'm' in text:
                        # Handle millions (M)
                        number = float(text.replace('m', '').strip())
                        return int(number * 1000000)
                    elif 'b' in text:
                        # Handle billions (B)
                        number = float(text.replace('b', '').strip())
                        return int(number * 1000000000)
                    else:
                        # Handle regular numbers with commas
                        return int(text.replace(',', ''))
                except:
                    return 0

            try:
                # Multiple selectors for follower counts
                follower_selectors = [
                    "span[role='button']",      # Modern layout
                    "div[class*='follower']",   # Alternative layout
                    "span[class*='follow']",    # Another variation
                    "div[class*='like']",       # Like count as fallback
                    "span[class*='like']",      # Another like variation
                    "a[role='link']"           # General links that might contain counts
                ]
                
                followers = 0
                for selector in follower_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        text = elem.text.lower()
                        if any(word in text for word in ['follower', 'like', 'follow']):
                            print(f"Found text: {text}")  # Debug print
                            
                            # Extract numbers with K/M/B suffixes
                            matches = re.findall(r'[\d,.]+[KkMmBb]?', text)
                            for match in matches:
                                num = convert_to_number(match)
                                if num > followers:  # Take the largest number found
                                    followers = num
                                    print(f"Converted {match} to {followers:,}")
                        
                        if followers > 0:
                            break
                    if followers > 0:
                        break
                    
                # Try to find category
                category_selectors = [
                    "a[role='link']",
                    "span[class*='category']",
                    "div[class*='category']",
                    "span[class*='type']",
                    "div[class*='type']"
                ]
                
                category = "Unknown"
                for selector in category_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for elem in elements:
                            text = elem.text.strip()
                            if text and len(text) < 50:  # Avoid getting long text
                                category = text
                                break
                    except:
                        continue

                print(f"Found followers: {followers:,}")  # Debug print
                
                if followers >= self.min_followers:
                    result = {
                        'name': page_data['name'],
                        'url': page_url,
                        'followers': followers,
                        'category': category,
                    }
                    print(f"✅ Qualifying page: {result['name']} with {followers:,} followers")
                    return result
                else:
                    print(f"❌ Page {page_data['name']} has only {followers:,} followers (minimum required: {self.min_followers:,})")
                
            except Exception as e:
                print(f"Error analyzing page content: {str(e)}")
                return None
                
        except Exception as e:
            print(f"Failed to analyze page {page_url}: {str(e)}")
            return None

    def save_results(self, filename='ethiopian_pages.csv'):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['name', 'url', 'followers', 'category'])
                writer.writeheader()
                writer.writerows(self.results)
            print(f"Results saved to {filename} - Total pages saved: {len(self.results)}")
        except Exception as e:
            print(f"Failed to save results: {str(e)}")

    def run_scraper(self, email, password, search_terms):
        try:
            if not self.login(email, password):
                return False

            total_pages_found = 0
            qualifying_pages = 0
            current_page = 0

            for term in search_terms:
                print(f"\nSearching for: {term}")
                pages = self.search_ethiopian_pages(term)
                total_pages_found += len(pages)
                
                for page_data in pages:
                    current_page += 1
                    print(f"\nProcessing page {current_page} of {total_pages_found}")
                    analyzed_data = self.analyze_page(page_data)
                    if analyzed_data:
                        self.results.append(analyzed_data)
                        qualifying_pages += 1
                        print(f"Added qualifying page: {analyzed_data['name']}")
                        print(f"Current progress: {qualifying_pages} qualifying pages found")
                        
                        # Save results after each successful addition
                        self.save_results()

            print(f"\nScraping completed!")
            print(f"Total pages found: {total_pages_found}")
            print(f"Qualifying pages (>={self.min_followers:,} followers): {qualifying_pages}")
            return True
        except Exception as e:
            print(f"Scraper error: {str(e)}")
            return False
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = FacebookPageScraper()
    
    # Get credentials from environment variables
    email = os.getenv('FACEBOOK_EMAIL')
    password = os.getenv('FACEBOOK_PASSWORD')
    
    if not email or not password:
        print("Error: Please set FACEBOOK_EMAIL and FACEBOOK_PASSWORD in .env file")
        exit(1)
    
    # Search terms
    search_terms = [
        "EBC Ethiopia",
        "Ethiopian Broadcasting Corporation",
        "Ethiopian News Channel",
        "Ethiopia Media Official",
        # Add more search terms as needed
    ]
    
    scraper.run_scraper(email, password, search_terms)