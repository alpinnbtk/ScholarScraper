# Project models
from models.scholarScraperConfig import ScholarScraperConfig
from models.scholarPaper import ScholarPaper

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class ScholarScraper:
    __BASE_URL = "https://scholar.google.com/scholar?hl=en"

    def __init__(self, query: str = "", config: ScholarScraperConfig = None):
        self.config = config or ScholarScraperConfig()
        
        if self.config._is_verbose:
            print("Initializing ScholarScraper...")

        # Internal state
        self.__query = None
        self.__query_array = []
        self.__query_url = ""
        self.__search_url = ""

        # Init webdriver (ALWAYS)
        self.__webdriver = self._init_webdriver()

        if query:
            self.set_query(query)

    # -------------------- Getters --------------------
    def get_query(self):
        return self.__query

    def get_query_array(self):
        return self.__query_array

    def get_query_url(self):
        return self.__query_url

    def get_search_url(self):
        return self.__search_url

    # -------------------- Setters --------------------
    def set_query(self, query: str):
        if not query:
            raise ValueError("Query cannot be empty or None.")
        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        self.__query = query
        self.__query_array = query.split()
        self.__query_url = "+".join(self.__query_array)
        self._build_search_url()

    def _build_search_url(self):
        self.__search_url = f"{self.__BASE_URL}&q={self.__query_url}"

        if self.config._is_verbose:
            print("Search URL built:")
            print(self.__search_url)

    # -------------------- WebDriver --------------------
    def _init_webdriver(
        self
    ):
        if self.config._is_verbose:
            print("Initializing Selenium WebDriver...")
        return webdriver.Chrome(options=self.config.apply_to_chrome_options())

    def _close_webdriver(self):
        if self.config._is_verbose:
            print("Closing Selenium WebDriver...")
        if self.__webdriver:
            self.__webdriver.quit()

    # -------------------- Status Check --------------------
    def check_request_status(self):
        if self.config._is_verbose:
            print("Checking request status...")

        if not self.__webdriver.title:
            return False

        if "scholar.google.com" not in self.__webdriver.current_url:
            return False

        return True

    # -------------------- Scraping Logic --------------------
    def request_scholar(self, query: str):
        if self.config._is_verbose:
            print(f"Scraping Google Scholar for query: {query}")

        self.set_query(query)
        self.__webdriver.get(self.get_search_url())

        if not self.check_request_status():
            raise RuntimeError("Failed to access Google Scholar.")

        if self.config._is_verbose:
            print("Page loaded successfully.")
            print("Title:", self.__webdriver.title)

    def _navigate_to_author_profile(self, author_name):
        try:
            profile_links = self.__webdriver.find_elements(By.CSS_SELECTOR, "h4.gs_rt2 a")
            for link in profile_links:
                if "citations?user=" in link.get_attribute("href"):
                    if author_name.lower() in link.text.lower():
                        link.click()
                        return True

            user_cards = self.__webdriver.find_elements(By.CSS_SELECTOR, "div.gsc_1usr h3.gs_rt a")
            for link in user_cards:
                if author_name.lower() in link.text.lower():
                    link.click()
                    return True

            if self.config._is_verbose: print("Author profile not found.")
            return False

        except Exception as e:
            if self.config._is_verbose: print(f"Error finding profile: {e}")
            return False

    def _scrape_modal_details(self):
        details = {
            "title": "", "link": "", "description": "", 
            "authors": "", "journal": "", "year": "", "citations": "0"
        }
        
        try:
            WebDriverWait(self.__webdriver, 10).until(
                EC.visibility_of_element_located((By.ID, "gsc_oci_table"))
            )

            try:
                title_elem = self.__webdriver.find_element(By.CSS_SELECTOR, "a.gsc_oci_title_link")
                details["title"] = title_elem.text
                details["link"] = title_elem.get_attribute("href")
            except:
                try: 
                    details["title"] = self.__webdriver.find_element(By.ID, "gsc_oci_title").text
                except: pass

            rows = self.__webdriver.find_elements(By.CSS_SELECTOR, "div.gs_scl")
            
            for row in rows:
                try:
                    label = row.find_element(By.CSS_SELECTOR, "div.gsc_oci_field").text.lower()
                    value = row.find_element(By.CSS_SELECTOR, "div.gsc_oci_value").text
                    
                    if "authors" in label:
                        details["authors"] = value
                    elif "publication date" in label:
                        details["year"] = value
                    elif "journal" in label:
                        details["journal"] = value
                    elif "description" in label:
                        details["description"] = value
                    elif "total citations" in label:
                        match = re.search(r'\d+', value)
                        if match: details["citations"] = match.group()
                except:
                    continue

        except Exception as e:
            if self.config._is_verbose: print(f"Error scraping details: {e}")
            
        return details

    def scrape_scholar_papers(self, count=10, output_format="dict"):
        papers = []

        if not self._navigate_to_author_profile(self.__query):
            return []

        for i in range(count):
            try:
                article_rows = WebDriverWait(self.__webdriver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.gsc_a_tr"))
                )
                
                if i >= len(article_rows):
                    break

                current_row = article_rows[i]
                
                title_link = current_row.find_element(By.CSS_SELECTOR, "a.gsc_a_at")
                title_link.click()
                
                data = self._scrape_modal_details()
                
                papers.append(ScholarPaper(
                    title=data["title"],
                    link=data["link"],
                    description=data["description"],
                    authors=data["authors"],
                    journal=data["journal"],
                    year=data["year"],
                    citations=data["citations"]
                ))
         
                try:
                    back_btn = WebDriverWait(self.__webdriver, 5).until(
                        EC.element_to_be_clickable((By.ID, "gs_hdr_bck"))
                    )
                    back_btn.click()
                except:
                    try:
                        self.__webdriver.find_element(By.ID, "gsc_oci_x").click()
                    except:
                        pass
                
                time.sleep(1)

            except Exception as e:
                if self.config._is_verbose: print(f"Error processing row {i}: {e}")
                try:
                    self.__webdriver.find_element(By.ID, "gs_hdr_bck").click()
                    time.sleep(1)
                except: pass
                continue

        if output_format=="json":
            return [paper.to_json() for paper in papers]
        
        if output_format=="dict":
            return [paper.to_dict() for paper in papers]