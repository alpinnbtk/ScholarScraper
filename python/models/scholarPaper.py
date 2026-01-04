import json

class ScholarPaper:
    def __init__(
        self,
        title: str,
        link: str,
        description: str,
        authors: str,
        publication_date: str,
        journal_name: str,
        number_of_citation: int
    ):
        self.set_title(title)
        self.set_link(link)
        self.set_description(description)
        self.set_authors(authors)
        self.set_publication_date(publication_date)
        self.set_journal_name(journal_name)
        self.set_number_of_citation(number_of_citation)

    def get_title(self) -> str:
        return self.__title

    def get_link(self) -> str:
        return self.__link

    def get_description(self) -> str:
        return self.__description

    def get_authors(self) -> str:
        return self.__authors
    
    def get_publication_date(self) -> str:
        return self.__publication_date

    def get_authors(self) -> str:
        return self.__authors
    
    def get_number_of_citation(self) -> int:
        return self.__number_of_citation
    
    def set_title(self, title: str):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string.")
        self.__title = title.strip()

    def set_link(self, link: str):
        if not isinstance(link, str) or not link.strip():
            raise ValueError("Link must be a non-empty string.")
        self.__link = link.strip()

    def set_description(self, description: str):
        if not isinstance(description, str):
            raise ValueError("Description must be a string.")
        self.__description = description.strip()

    def set_authors(self, authors: str):
        if not isinstance(authors, str):
            raise ValueError("Authors must be a string.")
        self.__authors = authors.strip()

    def set_publication_date(self, publication_date: str):
        if not isinstance(publication_date, str):
            raise ValueError("Publication Date must be a string.")
        self.__publication_date = publication_date.strip()

    def set_journal_name(self, journal_name: str):
        if not isinstance(journal_name, str):
            raise ValueError("Journal Name must be a string.")
        self.__journal_name = journal_name.strip()

    def set_number_of_citation(self, number_of_citation: int):
        if not isinstance(number_of_citation, int):
            raise ValueError("Number of Citation must be a number.")
        self.__number_of_citation = number_of_citation

    def to_dict(self) -> dict:
        return {
            "title": self.__title,
            "link": self.__link,
            "description": self.__description,
            "authors": self.__authors,
            "publication_date": self.__publication_date,
            "journal_name": self.__journal_name,
            "number_of_citation": self.__number_of_citation
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
            f"publication_date: {self.__publication_date}\n"
            f"journal_name: {self.__journal_name}\n"
            f"number_of_citation: {self.__number_of_citation}"
        )

    def __repr__(self) -> str:
        return (
            f"Paper(title={self.__title!r}, "
            f"link={self.__link!r}, "
            f"authors={self.__authors!r})"
        )
