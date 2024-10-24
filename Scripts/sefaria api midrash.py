from bs4 import BeautifulSoup
import requests

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def get_text(book, lang='en'):
    base_url = f"https://www.sefaria.org/api/texts/{book}"
    params = {
        'lang': lang,
        'commentary': 0,  # No commentary
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'text' in data:  # Check if 'text' key exists
            raw_text = data['text']
            cleaned_text = [clean_html(text) for text in raw_text]
            return cleaned_text
        else:
            print(f"'text' key not found for {book}")
            return None
    else:
        print(f"Failed to fetch {book}")
        return None

# Feasible Midrash sections
sections = [
    'Genesis_Rabbah', 'Exodus_Rabbah', 'Leviticus_Rabbah', 'Numbers_Rabbah', 'Deuteronomy_Rabbah',
    'Song_of_Songs_Rabbah', 'Ecclesiastes_Rabbah', 'Lamentations_Rabbah', 'Esther_Rabbah',
    'Sifrei_Numbers', 'Sifrei_Deuteronomy'
]

# Open a single file to store all sections
with open('Feasible_Midrash_Collection.txt', 'w', encoding='utf-8') as output_file:
    for section in sections:
        text = get_text(section)
        if text:
            output_file.write(f"Section: {section}\n")
            output_file.write('\n'.join(text))
            output_file.write('\n\n')  # Add spacing between sections
        else:
            print(f"Failed to download {section}")
