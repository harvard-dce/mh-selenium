
from time import sleep

def test_foo(mh_api, player):

    # play via canvas click
    player.find_by_css('#paella_plugin_PlayButtonOnScreen > canvas').click()
    sleep(1)
    # pause via canvas click
    player.find_by_css('#overlayContainer').click()
    sleep(1)

    # play via toolbar button
    player.find_by_css('#buttonPlugin0').click()
    sleep(1)
    # pause via toolbar button
    player.find_by_css('#buttonPlugin0').click()
    sleep(1)

    return
