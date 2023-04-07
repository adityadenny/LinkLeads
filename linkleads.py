from collections import deque
import re

from bs4 import BeautifulSoup
import requests
import urllib.parse


def is_valid_url(url):
    """
    Fungsi untuk memeriksa apakah URL valid
    """
    parts = urllib.parse.urlparse(url)
    return parts.scheme in ('http', 'https') and parts.netloc


def fix_url(url):
    """
    Fungsi untuk menambahkan skema URL (http/https) jika tidak ada
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url


user_url = input('[+] Masukkan URL: ')
user_url = fix_url(user_url)

urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0
limit = int(input('[+] Masukkan limit pencarian: '))

try:
    while urls:
        count += 1
        if count > limit:
            break

        url = urls.popleft()
        scraped_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = f'{parts.scheme}://{parts.netloc}'
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print(f'{count} Memproses {url}')

        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@\w+\.+[a-z\.]+', response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, 'html.parser')
        for anchor in soup.find_all('a'):
            link = anchor.attrs.get('href', '')
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link

            if not is_valid_url(link) or link in urls or link in scraped_urls:
                continue

            urls.append(link)

except KeyboardInterrupt:
    print('[-] Penelusuran dibatalkan.')

print('\n Proses selesai!')
print(f'\n{len(emails)} email ditemukan\n{"=" * 35}')

for mail in emails:
    print('  ' + mail)
print('\n')

# comment testinghjghjg