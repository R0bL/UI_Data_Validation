#!/usr/bin/env python3
"""
Quick test script to validate the crawler's specialized extraction functions.
Tests clinical trial, article, and other entity type extractions.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

def test_clinical_trial_extraction():
    """Test extraction on a clinical trial page."""
    print("\n" + "="*80)
    print("Testing Clinical Trial Page Extraction")
    print("="*80)

    driver = None
    try:
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to a clinical trial page
        test_url = "https://allsci.com/clinical-trial/ASC-CT-0000000000126-1.0-1734043206"
        print(f"\nNavigating to: {test_url}")
        driver.get(test_url)

        # Wait for page to load
        print("Waiting for page to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)  # Additional wait for dynamic content

        # Get page title
        page_title = driver.title
        print(f"Page Title: {page_title}")

        # Check for key elements
        print("\n--- Checking for Key Elements ---")

        # Check for header
        try:
            header = driver.find_element(By.CSS_SELECTOR, "div.header-card, div[class*='header']")
            print(f"✓ Header found: {header.text[:100]}...")
        except:
            print("✗ Header not found")

        # Check for cards
        try:
            cards = driver.find_elements(By.CSS_SELECTOR, "div.card, div[class*='card']")
            print(f"✓ Found {len(cards)} card elements")
        except:
            print("✗ No cards found")

        # Check for metadata
        try:
            metadata = driver.find_elements(By.CSS_SELECTOR, "div.metadata, div[class*='metadata']")
            print(f"✓ Found {len(metadata)} metadata elements")
        except:
            print("✗ No metadata found")

        # Get page source length
        page_source = driver.page_source
        print(f"\nPage source length: {len(page_source)} characters")

        # Check if page has content or is loading
        if "loading" in page_source.lower() or "skeleton" in page_source.lower():
            print("⚠ Page may still be loading (found loading/skeleton indicators)")
        else:
            print("✓ Page appears fully loaded")

        # Try to find specific clinical trial elements
        print("\n--- Clinical Trial Specific Elements ---")

        trial_elements = {
            "Trial Type Badge": "strong:contains('CLINICAL'), strong:contains('Clinical Trial')",
            "Timeline Section": "div[class*='timeline'], section[class*='timeline']",
            "Abstract Section": "div[class*='abstract'], section[class*='abstract']",
            "Metadata Section": "div[class*='metadata'], section[class*='metadata']",
            "Study Design": "div[class*='design'], section[class*='design']",
        }

        for element_name, selector in trial_elements.items():
            try:
                # Use more flexible CSS selectors
                if 'contains' in selector:
                    # Use XPath for text search
                    xpath = f"//*[contains(text(), 'CLINICAL') or contains(text(), 'Clinical Trial')]"
                    elements = driver.find_elements(By.XPATH, xpath)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)

                if elements:
                    print(f"✓ {element_name}: Found {len(elements)} elements")
                else:
                    print(f"✗ {element_name}: Not found")
            except Exception as e:
                print(f"✗ {element_name}: Error - {str(e)[:50]}")

        # Save a snapshot of the HTML for inspection
        snapshot_file = "/home/user/UI_Data_Validation/test_page_snapshot.html"
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"\n✓ Page HTML saved to: {snapshot_file}")

        print("\n" + "="*80)
        print("Test Complete")
        print("="*80)

    except Exception as e:
        print(f"\n✗ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()

def test_article_extraction():
    """Test extraction on an article page."""
    print("\n" + "="*80)
    print("Testing Article Page Extraction")
    print("="*80)

    driver = None
    try:
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to an article page
        test_url = "https://allsci.com/article/W4396737971"
        print(f"\nNavigating to: {test_url}")
        driver.get(test_url)

        # Wait for page to load
        print("Waiting for page to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)

        # Get page title
        page_title = driver.title
        print(f"Page Title: {page_title}")

        # Check for article-specific elements
        print("\n--- Article Specific Elements ---")

        article_elements = {
            "Article Type Badge": "span[class*='badge'], div[class*='type']",
            "Authors Section": "div[class*='author'], section[class*='author']",
            "Abstract": "div[class*='abstract'], section[class*='abstract']",
            "Citations": "div[class*='citation'], span[class*='citation']",
            "DOI": "div:contains('DOI'), span:contains('DOI')",
        }

        for element_name, selector in article_elements.items():
            try:
                if 'contains' in selector:
                    xpath = "//*[contains(text(), 'DOI')]"
                    elements = driver.find_elements(By.XPATH, xpath)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)

                if elements:
                    print(f"✓ {element_name}: Found {len(elements)} elements")
                else:
                    print(f"✗ {element_name}: Not found")
            except Exception as e:
                print(f"✗ {element_name}: Error - {str(e)[:50]}")

        print("\n" + "="*80)
        print("Test Complete")
        print("="*80)

    except Exception as e:
        print(f"\n✗ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    print("\n" + "="*80)
    print("AllSci Crawler - Extraction Function Tests")
    print("="*80)

    # Test clinical trial extraction
    test_clinical_trial_extraction()

    # Test article extraction
    test_article_extraction()

    print("\n✓ All tests completed")
