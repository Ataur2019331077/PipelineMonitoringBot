from bs4 import BeautifulSoup
import requests

def the_daily_sun():
    url = "https://www.daily-sun.com/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all the <a> tags
        a_tags = soup.find_all('a')

        headlines = []
        for a_tag in a_tags:
            # Extract headline from the alt attribute of the <img> tag
            img_tag = a_tag.find('img')
            if img_tag and 'alt' in img_tag.attrs:
                headline = img_tag['alt']
                link = f"https://www.daily-sun.com/{a_tag['href']}"
                headlines.append({'headline': headline, 'link': link})

        return headlines[:20]
    


def the_daily_star():
    url = "https://www.thedailystar.net/"
    response = requests.get(url)
    headlines = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all the <a> tags
        card_content_div = soup.find_all('div', class_='card-content')
        
        for div_tag in card_content_div:
            a_tags_in_card_content = div_tag.find_all('a')
            # Iterate over each <a> tag and get its parent <h3> tag
            for a_tag in a_tags_in_card_content:
                if a_tag.text != '':
                    headline = a_tag.text
                    link = f"https://www.thedailystar.net/{a_tag['href']}"
                    headlines.append({'headline': headline, 'link': link})

    
        return headlines[:20]  


def the_prothom_alo():
    url='https://en.prothomalo.com/'
    # Send a request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all news items
    news_items = soup.find_all('div', class_='news_with_item')

    # Extract headlines and links
    headlines_links = []
    for item in news_items:
        link_tag = item.find('a', href=True)
        if link_tag:
            headline = link_tag.get('aria-label')
            link = link_tag['href']
            if link.startswith('/'):
                link = url + link  # Convert relative link to absolute link
            headlines_links.append({'headline': headline, 'link': link})

    return headlines_links


