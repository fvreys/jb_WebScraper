import requests
from bs4 import BeautifulSoup
import string
import os

"""
Create a program that takes the https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3  URL 
and then goes over the page source code searching for articles.
Detect the article type and the link to view the article tags and their attributes.
Save the contents of each article of the type "News", that is, the text from the article body without the tags, 
to a separate file named %article_title%.txt. When you save the file, replace the whitespaces in the name 
of the article with underscores and remove punctuation marks in the filename. 
Use string.punctuation to remove punctuation. 
Strip all trailing whitespaces in the article body and title. 
(Optional) You may output some result message once the saving is done, but it is not required.
Make sure your output file is binary with the UTF-8 character encoding. 
"""

def sanitize_filename(title: str) -> str:
    cleaned = title.strip().translate(str.maketrans("", "", string.punctuation))
    cleaned = "_".join(cleaned.split())
    return cleaned


def main() -> None:
    """

    :rtype: None
    """
    nr_pages = int(input())
    article_type_input = input()

    headers = {'Accept-Language': 'en-US,en;q=0.5'}
    base_url = "https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020"

    for page in range(1, nr_pages + 1):
        page_folder = f"Page_{page}"
        os.makedirs (page_folder, exist_ok=True)

        url_search = f"{base_url}&page={page}"
        response = requests.get(url_search, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for article in soup.find_all("article"):
            article_type_tag = article.find("span", attrs={'data-test': "article.type"})
            if article_type_tag is None:
                continue

            article_type = article_type_tag.get_text(strip=True)
            if article_type != article_type_input:
                continue

            title_tag = article.find("a", class_="c-card__link")
            if title_tag is None:
                continue

            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            if link is None:
                continue

            article_url = f"https://www.nature.com{link}"
            article_response = requests.get(article_url, headers=headers)
            article_soup = BeautifulSoup(article_response.text, "html.parser")

            teaser = article_soup.find ("p", class_="article__teaser")
            if teaser is None:
                continue

            article_body = teaser.get_text(strip=True)
            if not article_body:
                continue

            filename = os.path.join(page_folder, f"{sanitize_filename (title)}.txt")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(article_body)

if __name__ == "__main__":
    main()
