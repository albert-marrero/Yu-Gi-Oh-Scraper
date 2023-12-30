from yugioh_scraper.yugipedia import scrape_set_categories, scrape_cards

def test_scrape_set_categories():
    # Test that the function returns a list
    assert type(scrape_set_categories()) == list

def test_scrape_tcg_cards():
    # Test that the function returns a list
    assert scrape_cards('https://yugipedia.com/index.php?title=Category:TCG_cards') == None
