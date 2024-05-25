from bs4 import BeautifulSoup
import os
from fiverr_api import session

base_url = "https://www.fiverr.com"

def process_html_files(base_path):
    session.set_scraper_api_key("cb672d07ab5658311e8958cc0dfffe13")
    for category in os.listdir(base_path):
        category_path = os.path.join(base_path, category)
        if os.path.isdir(category_path):
            for field in os.listdir(category_path):
                field_path = os.path.join(category_path, field)
                if os.path.isdir(field_path):
                    for file_name in ["0.html", "1.html", "2.html", "3.html"]:
                        file_path = os.path.join(field_path, file_name)
                        if os.path.isfile(file_path):
                            with open(file_path, "r", encoding="utf-8") as file:
                                html_content = file.read()
                            soup = BeautifulSoup(html_content, "html.parser")
                            item_divs = soup.find_all("div", class_="gig-card-layout")
                            item_links = []
                            for div in item_divs:
                                link = div.find_all("a", href=True)[2]
                                if link:
                                    item_links.append(base_url + link["href"])
                            seller_levels = ["new_seller", "level_1", "level_2", "top_rated_seller"]
                            seller_level = seller_levels[int(file_name[0])]
                            level_folder_path = os.path.join("items_htmls",category, field,seller_level)
                            os.makedirs(level_folder_path, exist_ok=True)
                            for index, link in enumerate(item_links):
                                try:
                                    response = session.get(link)
                                    html_file_path = os.path.join(level_folder_path, f"{index + 1}.html")
                                    with open(html_file_path, 'w', encoding='utf-8') as html_file:
                                        html_file.write(str(response.soup))
                                except Exception as e:
                                    print(f"Error processing {link}: {e}")


base_path = "htmls"
process_html_files(base_path)