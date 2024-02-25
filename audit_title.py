import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
import sys

def get_urls_from_sitemap(sitemap_url):
    urls = []
    try:
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            sitemap = ET.fromstring(response.content)
            for url in sitemap.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                urls.append(loc)
        else:
            print(f'Error: No se pudo acceder a {sitemap_url}')
    except Exception as e:
        print(f'Error al procesar el sitemap {sitemap_url}: {e}')

    return urls

def audit_title_and_meta(urls):
    with open('audit_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['URL', 'Title', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for url in urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.find('title')
                    meta_description = soup.find('meta', attrs={'name': 'description'})

                    title_text = title.text if title else 'No encontrado'
                    description_text = meta_description.get("content", "No encontrado") if meta_description else 'No encontrado'

                    writer.writerow({'URL': url, 'Title': title_text, 'Description': description_text})
                else:
                    writer.writerow({'URL': url, 'Title': 'Error de acceso', 'Description': 'Error de acceso'})
            except Exception as e:
                writer.writerow({'URL': url, 'Title': 'Error al procesar', 'Description': str(e)})

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sitemap_url = sys.argv[1]
        urls = get_urls_from_sitemap(sitemap_url)
        audit_title_and_meta(urls)
    else:
        print("Por favor, proporciona la URL del sitemap como argumento.")

