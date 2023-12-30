from yugioh_scraper.yugipedia import get_card_info, scrape_set_categories, scrape_cards

# def test_scrape_set_categories():
#     # Test that the function returns a list
#     assert type(scrape_set_categories()) == list

# def test_scrape_tcg_cards():
#     # Test that the function returns a list
#     assert scrape_cards('https://yugipedia.com/index.php?title=Category:TCG_cards') == None

def test_normal_monster_cards():
    card_name = 'Megalosmasher X'
    get_card_info(card_name)

def test_effect_monster_cards():
    card_name = 'B.E.S. Big Core MK-3'
    get_card_info(card_name)

def test_fusion_monster_cards():
    card_name = 'Neo Blue-Eyes Ultimate Dragon'
    get_card_info(card_name)

def test_ritual_monster_cards():
    card_name = 'Vennu, Bright Bird of Divinity'
    get_card_info(card_name)

def test_synchro_monster_cards():
    card_name = 'Trishula, Dragon of the Ice Barrier'
    get_card_info(card_name)

def test_xyz_monster_cards():
    card_name = 'Cyber Dragon Infinity'
    get_card_info(card_name)

def test_pendulum_monster_cards():
    card_name = 'Odd-Eyes Pendulum Dragon'
    get_card_info(card_name)

def test_link_monster_cards():
    card_name = 'Decode Talker'
    get_card_info(card_name)

def test_token_monster_cards():
    card_name = 'Dragon Lord Token'
    get_card_info(card_name)


