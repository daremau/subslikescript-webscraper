import requests
from bs4 import BeautifulSoup

def get_html(text):
  root = 'https://subslikescript.com'
  website = f'{root}/{text}'
  response = requests.get(website)
  content = response.text

  return BeautifulSoup(content, "lxml")

soup = get_html('movies')

#Pagination
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('a', class_='page-link')
last_page = pages[-2].text


for page in range(1, int(last_page) + 1):
  print(page)
  soup = get_html(f'/movies?page={page}')

  box = soup.find('article', class_='main-article')

  #Getting links of the movies
  links = []
  for link in box.find_all('a', href=True):
    links.append(link['href'])

  #Getting the script of the movie
  for link in links:
    try:
      print(link)
      soup = get_html(link)

      box = soup.find('article', class_='main-article')
      title = box.find('h1').get_text()
      transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')
      
      with open(f'./files/{title}.txt', 'w', encoding='utf-8') as file:
        file.write(transcript)
      
    except:
      print(f'------Link not working: {link}-------')
