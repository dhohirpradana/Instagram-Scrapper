import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')

# options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-extensions")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-features=VizDisplayCompositor")
# options.add_argument("--disable-features=NetworkService")
# # , firefox_binary=binary

# driver = webdriver.Firefox(options=options)


def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    chrome_prefs = dict[str, dict[str, int]]()
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


driver = webdriver.Chrome(options=set_chrome_options())
driver.delete_all_cookies()
# BASE_DIR = os.path.join(os.path.dirname(__file__), '..')


def handler(request, jsonify):
    body = request.get_json()

    if body is None:
        return jsonify({'message': 'No body provided'}), 400

    try:
        query = body['keyword']
        max_count = body['max_count']
    except AttributeError as err:
        return jsonify({'message': str(err) + " not provided"}), 400

    query_url = urllib.parse.quote(query)
    print('Query URL: ', query_url)
    
    img_alts = []

    try:
        driver.get(f"https://www.instagram.com/explore/tags/{query_url}")

        scroll_height = driver.execute_script("return window.innerHeight")

        # while True:
        while len(img_alts) < max_count:
            # feeds class = _aagv
            feeds = driver.find_elements(By.CLASS_NAME, "_aagv")
            # print("feed: ", feeds)
            
            for feed in feeds:
                # print("feed: ", feed)
                img_alt = feed.find_element(By.TAG_NAME, "img").get_attribute("alt")
                print("img_alt: ", img_alt)
                
                if len(img_alts) >= max_count:
                    break
                
                img_alts.append(img_alt)
                # link = feed.find_element(By.TAG_NAME, "a").get_attribute("href")
                # print("link: ", link)
                # feed.click()
                # time.sleep(2)
                # driver.back()
                # time.sleep(2)

            document_height_before = driver.execute_script(
                "return document.documentElement.scrollHeight")
            driver.execute_script(
                f"window.scrollTo(0, {document_height_before + scroll_height});")

            # delay before next scroll
            time.sleep(2)
            document_height_after = driver.execute_script(
                "return document.documentElement.scrollHeight")

            # end of scroll
            if document_height_after == document_height_before:
                break

    except ConnectionError as err:
        print("Error: ", err)
        return jsonify({'message': str(err)}), 500

    return jsonify({'message': 'success', "results": img_alts}), 200
