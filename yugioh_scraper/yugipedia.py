import yugioh_scraper.logging_config

import logging
import time

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def scrape_set_categories():
    """
    Scrape all sets from Yugipedia and return a list of set names.
    """
    logger.info('Scraping all sets from Yugipedia...')
    
    # Set the URL to scrape
    url = 'https://yugipedia.com/wiki/Category:TCG_sets'
    logger.debug(f'Setting TCG set URL to {url}')

    # Set the user agent to avoid getting blocked
    headers = {'User-agent': 'Mozilla/5.0'}
    logger.debug(f'Setting headers to {headers}')

    # Make a GET request to the URL
    response = requests.get(url, headers=headers)
    logger.debug(f'Response status code: {response.status_code}')

    # if response is anything other than 200, log an error and raise an exception
    if response.status_code != 200:
        logger.error('Response status code was not 200.')
        raise Exception('Response status code was not 200.')
    
    # Parse the HTML response
    logger.debug('Parsing HTML response...')
    soup = BeautifulSoup(response.content, 'html.parser')
    set_categories = soup.find_all(class_='CategoryTreeItem')
    # Count the number of set categories
    logger.info(f'Found {len(set_categories)} set categories.')

    # Create empty list to store set categories urls
    logger.debug('Creating empty list to store set categories urls...')
    set_categories_urls = []
    logger.debug(f'Created empty list: {set_categories_urls}')
    
    # Loop through each set category
    logger.debug('Looping through each set category...')
    for category in set_categories:
        # Find all links in the set category
        logger.debug('Finding all links in the set category...')
        categories = category.find_all('a')
        # Add the first link to the set categories urls list
        logger.debug('Adding the first link to the set categories urls list...')
        set_categories_urls.append(categories[0]['href'])
        logger.debug(f'Added {categories[0]["href"]} to the set categories urls list.')
    logger.debug('Successfully looped through each set category.')
    logger.info('Successfully parsed HTML response.')
    logger.info('Successfully scraped all sets from Yugipedia.')
    logger.debug(f'Set categories urls: {set_categories_urls}')
    return set_categories_urls

def scrape_cards(url):
    """
    Scrape all cards from a set and return a list of card names.
    """

    logger.info('Scraping all cards from Yugipedia...')

    # Set start time to calculate how long it takes to scrape all cards
    start_time = time.time()
    logger.debug(f'Start time: {start_time}')
    
    # Set the URL to scrape
    logger.info(f'Setting TCG Cards URL to {url}')

    # Set the user agent to avoid getting blocked
    headers = {'User-agent': 'Mozilla/5.0'}
    logger.debug(f'Setting headers to {headers}')

    # Make a GET request to the URL
    response = requests.get(url, headers=headers)
    logger.debug(f'Response status code: {response.status_code}')

    # if response is anything other than 200, log an error and raise an exception
    if response.status_code != 200:
        logger.error('Response status code was not 200.')
        raise Exception('Response status code was not 200.')
    
    # Parse the HTML response
    logger.debug('Parsing HTML response...')
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all elements with class mw-category-group and a tags
    card_group = soup.find_all(class_='mw-category-group')
    logger.debug(f'Found {len(card_group)} card groups.')

    while True:
    
        # if length of card group is 0, break out of the loop
        if len(card_group) == 0:
            logger.debug('Length of card group was 0.')
            logger.info('Successfully scraped all cards from Yugipedia.')

            # Set end time to calculate how long it takes to scrape all cards
            end_time = time.time()
            logger.debug(f'End time: {end_time}')
            
            # Calculate how long it took to scrape all cards
            logger.debug('Calculating how long it took to scrape all cards...')
            total_time = end_time - start_time
            logger.info(f'Total time to scrape all cards: {total_time}')

            break

        else:
            # Create empty list to store card urls and card names
            logger.debug('Creating empty list to store card urls and card names as a JSON object...')
            card_list = list()

            # Loop through each card group
            logger.debug('Looping through each card group...')
            for group in card_group:
                # Find all links in the card group
                logger.debug('Finding all links in the card group...')
                cards = group.find_all('a')
                # Loop through each card
                logger.debug('Looping through each card...')
                for card in cards:
                    # Add the card name and url to the card list
                    logger.debug('Adding the card name and url to the card list...')
                    card_list.append({
                        'name': card.text,
                        'url': card['href']
                    })
                    logger.debug(f'Added {card.text} to the card list.')
                logger.debug('Successfully looped through each card.')
            logger.debug('Successfully looped through each card group.')

            # Get Last object in card list
            logger.debug('Getting last object in card list...')
            last_card = card_list[-1]
            logger.debug(f'Last object in card list: {last_card}')

            # Build next page URL
            logger.debug('Building next page URL...')
            # Get the last card name
            last_card_name = last_card['name']
            logger.debug(f'Last card name: {last_card_name}')
            # Swap spaces with plus symbols
            last_card_name = last_card_name.replace(' ', '+')
            logger.debug(f'Last card name with plus symbols: {last_card_name}')
            # Build next page URL
            next_page_url = f'https://yugipedia.com/index.php?title=Category:TCG_cards&pagefrom={last_card_name}#mw-pages'
            logger.info(f'Next page URL: {next_page_url}')

            # sleep for 5 seconds to avoid getting blocked
            logger.debug('Sleeping for 5 seconds...')
            time.sleep(5)
            logger.debug('Successfully slept for 5 seconds.')

            # Recursively call scrape_cards() with next page URL
            logger.debug('Recursively calling scrape_cards() with next page URL...')
            scrape_cards(next_page_url)
            logger.debug('Successfully recursively called scrape_cards() with next page URL.')