import requests
from bs4 import BeautifulSoup


def get_articles(keywords):
    keywords_set = set(keywords)
    response = requests.get("https://habr.com/ru/articles/")
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features="html.parser")
    articles = soup.find_all("article")

    if not articles:
        print("Статьи не найдены!")
        return

    print(f"Количество статей найдено: {len(articles)}")

    for article in articles:
        header = article.find("h2")
        header_text = header.text.strip() if header else "Нет заголовка"

        public_date = article.find("time")
        public_date_text = (
            public_date["datetime"]
            if public_date and public_date.has_attr("datetime")
            else "Нет даты"
        )

        post_link_elem = header.find("a")
        post_link = (
            "https://habr.com" + post_link_elem["href"]
            if post_link_elem and post_link_elem.has_attr("href")
            else "Нет ссылки"
        )

        if post_link == "Нет ссылки":
            print(f"Ошибка: не удалось получить ссылку для заголовка '{header_text}'")
            continue

        article_text = get_article_text(post_link)

        if any(keyword.lower() in article_text.lower() for keyword in keywords_set):
            print(f"{public_date_text} – {header_text} – {post_link}")


def get_article_text(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features="html.parser")

    article_body = soup.find("div", class_="tm-article-body")
    return article_body.text.strip() if article_body else ""


if __name__ == "__main__":
    KEYWORDS = ["дизайн", "фото", "web", "python"]

    get_articles(KEYWORDS)
