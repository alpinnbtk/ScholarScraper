# Project models
from models.scholarScraperConfig import ScholarScraperConfig
from models.scholarPaper import ScholarPaper

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScholarScraper:
    __BASE_URL = "https://scholar.google.com/scholar?hl=en"

    def __init__(self, author: str = "", query: str = "", config: ScholarScraperConfig = None):
        self.config = config or ScholarScraperConfig()
        
        if self.config._is_verbose:
            print("Initializing ScholarScraper...")

        # Internal state
        self.__author = None
        self.__query = None
        self.__query_array = []
        self.__query_url = ""
        self.__search_url = ""

        # Init webdriver (ALWAYS)
        self.__webdriver = self._init_webdriver()

        if author:
            self.set_author(author)

        if query:
            self.set_query(query)

    # -------------------- Getters --------------------
    def get_author(self):
        return self.__author
    
    def get_query(self):
        return self.__query

    def get_query_array(self):
        return self.__query_array

    def get_query_url(self):
        return self.__query_url

    def get_search_url(self):
        return self.__search_url

    # -------------------- Setters --------------------
    def set_author(self, author: str):
        if not author:
            raise ValueError("Author cannot be empty or None.")
        if not isinstance(author, str):
            raise TypeError("Author must be a string.")

        self.__author = author
        self.__author_array = author.split()
        self.__author_url = "+".join(self.__author_array)
        self._build_search_url()

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
        parts = []

        if self.__author:
            parts.append(self.__author_url)

        else:
            parts.append(self.__query_url)

        q = "+".join(parts)

        self.__search_url = f"{self.__BASE_URL}&q={q}"

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

    # def scrape_paper_authors(self, paper_node):
    #     try:
    #         authors_info = paper_node.find_element(By.CSS_SELECTOR, "div.gs_a").text
    #         authors = authors_info.split("-")[0].strip()
    #         return authors
    #     except Exception:
    #         return "Unknown"
        
    # def scrape_scholar_papers(self, count=10,output_format="dict"):
    #     papers = []

    #     WebDriverWait(self.__webdriver, 15).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, "div.gs_ri"))
    #     )

    #     results = self.__webdriver.find_elements(By.CSS_SELECTOR, "div.gs_ri")

    #     for node in results[:count]:
    #         title = node.find_element(By.CSS_SELECTOR, "a")
    #         title_result = title.text
    #         link_result = title.get_attribute("href")
    #         authors = self.scrape_paper_authors(node)
    #         description = node.find_element(By.CSS_SELECTOR, "div.gs_rs").text.strip()
    #         papers.append(ScholarPaper(title_result, link_result, description, authors))

    #     if output_format=="json":
    #         return [paper.to_json() for paper in papers]
        
    #     if output_format=="dict":
    #         return [paper.to_dict() for paper in papers]
        
    # -------------------- Scraping Logic (NEW) --------------------
    def request_scholar(self, author: str, query: str):
        if self.config._is_verbose:
            print(f"Scraping Google Scholar for author: {author} with query: {query}")

        self.set_query(query)
        self.set_author(author)
        self.__webdriver.get(self.get_search_url())

        if not self.check_request_status():
            raise RuntimeError("Failed to access Google Scholar.")

        if self.config._is_verbose:
            print("Page loaded successfully.")
            print("Title:", self.__webdriver.title)

    def access_author_page(self):
        WebDriverWait(self.__webdriver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h4.gs_rt2 a"))
        )

        link = self.__webdriver.find_element(By.CSS_SELECTOR, "h4.gs_rt2 a").get_attribute("href")

        if link.startswith("/"):
            link = "https://scholar.google.com" + link

        self.__webdriver.get(link)
        return link


    def access_paper_page(self, link):
        self.__search_url = link

        self.__webdriver.get(self.get_search_url())

        WebDriverWait(self.__webdriver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.gsc_oci_title"))
        )

        title = self.__webdriver.find_elements(By.CSS_SELECTOR, "div.gsc_oci_title")

        if title:
            paper = title[0].find_element(By.CSS_SELECTOR, "a")
            paper_title = paper.text
            paper_link = paper.get_attribute("href")

        results = self.__webdriver.find_elements(By.CSS_SELECTOR, "div.gs_oci_value")

        authors = results[0].text
        publication_date = results[1].text
        journal_name = results[2].text
        description = results[6].text
        citation = results[7].find_element(By.CSS_SELECTOR, "a")
        citation_text = citation.text
        number_of_citation = "".join(filter(str.isdigit, citation_text))

        article = ScholarPaper(paper_title, paper_link, description, authors, publication_date, journal_name, number_of_citation)

        return article

    def scrape_article_page(self):
        try:
            title_anchor = self.__webdriver.find_element(
                By.CSS_SELECTOR, "a.gsc_oci_title_link"
            )
            title_result = title_anchor.text
            link = title_anchor.get_attribute("href")
        except:
            title_div = self.__webdriver.find_element(By.ID, "gsc_oci_title")
            title_result = title_div.text
            link = ""

        values = self.__webdriver.find_elements(By.CSS_SELECTOR, "div.gsc_oci_value")

        authors = values[0].text if len(values) > 0 else ""
        publication_date = values[1].text if len(values) > 1 else ""
        journal_name = values[2].text if len(values) > 2 else ""
        description = values[6].text if len(values) > 6 else ""

        citation_text = ""
        if len(values) > 7:
            citation_text = values[7].find_element(By.TAG_NAME, "a").text

        number_of_citation = "".join(filter(str.isdigit, citation_text))

        return ScholarPaper(
            title=title_result,
            link=link, 
            description=description,
            authors=authors,
            publication_date=publication_date,
            journal_name=journal_name,
            number_of_citation = int(number_of_citation) if number_of_citation else 0
        )



    def scrape_paper_authors(self, paper_node):
        try:
            authors_info = paper_node.find_element(By.CSS_SELECTOR, "div.gs_a").text
            authors = authors_info.split("-")[0].strip()
            return authors
        except Exception:
            return "Unknown"
        
    def scrape_scholar_papers(self, count=10,output_format="dict"):
        papers = []

        WebDriverWait(self.__webdriver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.gsc_a_tr"))
        )

        rows = self.__webdriver.find_elements(By.CSS_SELECTOR, "tr.gsc_a_tr")

        for row in rows[:count]:
            title_link = row.find_element(By.CSS_SELECTOR, "a.gsc_a_at")

            # CLICK (INI PENTING)
            self.__webdriver.execute_script(
                "arguments[0].click();", title_link
            )

            # TUNGGU HALAMAN DETAIL
            WebDriverWait(self.__webdriver, 15).until(
                EC.presence_of_element_located((By.ID, "gsc_oci_title"))
            )

            article = self.scrape_article_page()
            papers.append(article)

            # KEMBALI KE AUTHOR PAGE
            self.__webdriver.back()

            WebDriverWait(self.__webdriver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr.gsc_a_tr"))
            )

        if output_format=="json":
            return [paper.to_json() for paper in papers]
        
        if output_format=="dict":
            return [paper.to_dict() for paper in papers]
        
    

