"""
Tests that the Live Monitor page contains a video table element and that the table
has at least one row
"""

def test_live_mon(admin_browser):

    admin_browser.find_by_id('adminlink').click()
    admin_browser.find_by_css('#pageHeader > a:nth-child(1)').click()

    video_table = admin_browser.find_by_css('#tabsWrapper > div.ng-scope > table')
    assert len(video_table) > 0

    video_table_rows = admin_browser.find_by_css('#tabsWrapper > div.ng-scope > table > tbody > tr')
    assert len(video_table_rows) > 0