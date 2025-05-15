import csv
import requests  # Предполагаем, что разрешено
from bs4 import BeautifulSoup  # Предполагаем, что разрешено
from collections import Counter  # Для удобного подсчета
import time  # Для небольшой задержки между запросами

BASE_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"



def fetch_page_content(url: str) -> str | None:
    """Получает HTML-содержимое страницы."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        return None


def parse_animal_page(html_content: str) -> tuple[list[str], str | None]:
    """
    Парсит HTML-содержимое страницы категории.
    Возвращает список имен животных на странице и URL следующей страницы (или None).
    """
    soup = BeautifulSoup(html_content, "html.parser")
    animal_names = []

    category_groups = soup.select(".mw-category-columns ul li a")
    for link in category_groups:
        animal_name = link.text.strip()
        if animal_name:  # Убедимся, что имя не пустое
            animal_names.append(animal_name)

    # Поиск ссылки на следующую страницу
    next_page_link_tag = soup.find("a", string="Следующая страница")

    next_page_url = None
    if next_page_link_tag and next_page_link_tag.get("href"):
        next_page_url = 'https://ru.wikipedia.org' + next_page_link_tag["href"]

    return animal_names, next_page_url


def get_all_animals_by_first_letter() -> Counter:
    """
    Собирает всех животных со страниц категории и подсчитывает их по первой букве.
    """
    animal_counts = Counter()
    current_url = BASE_URL
    page_num = 0

    while current_url:
        page_num += 1
        print(f"Обработка страницы {page_num}")

        html_content = fetch_page_content(current_url)
        if not html_content:
            print(f"Не удалось получить содержимое страницы {current_url}. Пропускаем.")
            break

        animal_names_on_page, next_url = parse_animal_page(html_content)

        if not animal_names_on_page and not next_url and page_num > 1:
            print(f"На странице {current_url} не найдено животных или ссылки на следующую. Возможно, конец.")

        for name in animal_names_on_page:
            if name:
                first_letter = name[0].upper()
                if 'А' <= first_letter <= 'Я' or first_letter == 'Ё':
                    animal_counts[first_letter] += 1

        current_url = next_url

    return animal_counts


def save_to_csv(data: Counter, filename: str = "beasts.csv"):
    """Сохраняет подсчитанные данные в CSV-файл."""
    if not data:
        print("Нет данных для сохранения.")
        return

    sorted_data = sorted(data.items())

    try:
        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            for letter, count in sorted_data:
                writer.writerow([letter, count])
        print(f"Данные успешно записаны в {filename}")
    except IOError as e:
        print(f"Ошибка при записи в файл {filename}: {e}")


def get_result():
    animal_stats = get_all_animals_by_first_letter()
    if animal_stats:
        save_to_csv(animal_stats)
    else:
        print("Не удалось собрать данные о животных.")