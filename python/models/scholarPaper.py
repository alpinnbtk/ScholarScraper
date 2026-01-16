import json

class ScholarPaper:
    def __init__(
        self,
        title: str,
        link: str,
        description: str,
        authors: str,
        journal: str,
        year: str,
        citations: str
    ):
        self.set_title(title)
        self.set_link(link)
        self.set_description(description)
        self.set_authors(authors)
        self.set_journal(journal)
        self.set_year(year)
        self.set_citations(citations)

    # -------------------- Getters --------------------
    def get_title(self) -> str:
        return self.__title

    def get_link(self) -> str:
        return self.__link

    def get_description(self) -> str:
        return self.__description

    def get_authors(self) -> str:
        return self.__authors

    def get_journal(self) -> str:
        return self.__journal

    def get_year(self) -> str:
        return self.__year

    def get_citations(self) -> str:
        return self.__citations
    
    # -------------------- Setters --------------------
    def set_title(self, title: str):
        if not isinstance(title, str) or not title.strip():
            self.__title = title.strip() if isinstance(title, str) else "Unknown Title"
        else:
            self.__title = title.strip()

    def set_link(self, link: str):
        if not isinstance(link, str):
            self.__link = ""
        else:
            self.__link = link.strip()

    def set_description(self, description: str):
        if not isinstance(description, str):
            self.__description = ""
        else:
            self.__description = description.strip()

    def set_authors(self, authors: str):
        if not isinstance(authors, str):
            self.__authors = ""
        else:
            self.__authors = authors.strip()

    def set_journal(self, journal: str):
        if not isinstance(journal, str):
            self.__journal = ""
        else:
            self.__journal = journal.strip()

    def set_year(self, year: str):
        if not isinstance(year, str):
            self.__year = ""
        else:
            self.__year = year.strip()

    def set_citations(self, citations: str):
        if not isinstance(citations, str):
            self.__citations = "0"
        else:
            self.__citations = citations.strip()

    def to_dict(self) -> dict:
        return {
            "title": self.__title,
            "link": self.__link,
            "description": self.__description,
            "authors": self.__authors,
            "journal": self.__journal,
            "year": self.__year,
            "citations": self.__citations
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False,
        )

    def __str__(self) -> str:
        return (
            f"title: {self.__title}\n"
            f"link: {self.__link}\n"
            f"description: {self.__description}\n"
            f"authors: {self.__authors}\n"
            f"journal: {self.__journal}\n"
            f"year: {self.__year}\n"
            f"citations: {self.__citations}"
        )

    def __repr__(self) -> str:
        return (
            f"Paper(title={self.__title!r}, "
            f"authors={self.__authors!r}, "
            f"journal={self.__journal!r}, "
            f"year={self.__year!r})"
        )