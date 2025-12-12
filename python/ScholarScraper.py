# Project models
import ProjectConfig
import Paper

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ScholarScraper:
    __url = "https://scholar.google.com/scholar?hl=en"

    def __init__(self):
        if ProjectConfig._is_verbose:
            print("Initializing ScholarScraper...")
            self.__webdriver = self._init_webdriver()

    # Getters
    def get_query(self):
        return self.__query
    
    def get_guery_array(self):
        return self.__query_array
    
    def get_query_url(self):
        return self.__query_url
    
    def get_search_url(self):
        return self.__search_url
    
    # Setters
    def set_query(self, query):
        if not query: 
            raise ValueError("Query cannot be empty or None.")
        if not isinstance(query, str):
            raise TypeError("set_query_error(): Query must be a string, not an array.")
        self.__query = query
        self.set_query_array(query.split(" "))
        self.set_query_url("+".join(self.query_array))


    def set_query_array(self, query_array):
        if query_array is None or len(query_array) == 0:
            raise ValueError("Query array cannot be empty or None.")
        if query_array is not list:
            raise TypeError("Query array must be a list of strings, not a single string.")
        self.__query_array = query_array
        
    def set_query_url(self, query_url):
        if query_url is None or query_url == "":
            raise ValueError("Query URL cannot be empty or None.")
        if query_url is not str:
            raise TypeError("Query URL must be a string, not an array.")
        self.__query_url = query_url
        
    def _set_search_url(self, search_url):
        if search_url is None or search_url == "":
            raise ValueError("Search URL cannot be empty or None.")
        if search_url is not str:
            raise TypeError("Search URL must be a string, not an array.")
        self.__search_url = search_url
    
    # Initiallize WebDriver
    def _init_webdriver(self):
        if ProjectConfig._is_verbose:
            print("Initializing Selenium Web Driver...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--remote-allow-origins=*")
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def _close_webdriver(self):
        if ProjectConfig._is_verbose:
            print("Closing Selenium Web Driver...")
        if self.__webdriver:
            self.__webdriver.quit()
    
    def check_request_status(self):
        if ProjectConfig._is_verbose:
            print("Checking request status...")
        if self.__webdriver.title == "" and not self.__webdriver.current_url. contains("scholar.google.com"):
            return False
        return True
    
    # Scrapping logic 
    def scrape_scholar(self, query):
        if ProjectConfig._is_verbose:
            print(f"Scraping Google Scholar for query: {query}")
        self.set_query(query)
        self._set_search_url(f"{self.__url}&q={self.get_query_url()}")
        self.__webdriver.get(self.get_search_url())
        if not self.check_request_status():
            raise Exception("Failed to access Google Scholar.")
                        
        if ProjectConfig._is_verbose:
            print(f"Accessed URL: {self.get_search_url()}")

    

# Test
try:
    scraper = ScholarScraper()
    scraper.scrape_scholar("machine learning")
except Exception as e:
    print(f"An error occurred:",e,sep="\n")
finally:
    scraper._close_webdriver()