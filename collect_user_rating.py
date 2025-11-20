import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
from dotenv import load_dotenv
from protego import Protego

load_dotenv()

user_agent = os.getenv('USER_AGENT')
HEADERS = {'user-agent': user_agent}
url = 'https://www.allmovie.com'
response = requests.get(url + '/robots.txt', headers=HEADERS)
rp = Protego.parse(response.text)


options = Options()
# options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
prefs = {
    "profile.default_content_setting_values": {
        "images": 2,
        "stylesheet": 2,
        "fonts": 2, 
        "javascript": 1  
    }
}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)

seen_user = set()

try:
    with open('users.jsonl', 'r') as lines:
        for line in lines:
            data = json.loads(line)
            movie_id = data.get('id')
            if movie_id:
                seen_user.add(movie_id)
except:
    pass

try:
    with open('data.jsonl', 'r') as lines, open('users.jsonl', 'a') as file:
        for line in lines:
            data = json.loads(line)
            movie_id = data.get('id')
            url = data.get('url')
            if movie_id not in seen_user:
                if rp.can_fetch(url, user_agent):
                    driver.get(url)
                    flag = False
                    try:
                        user_count = int(WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".average-user-rating-count"))
                        ).text)
                        user_rating_elem = driver.find_element(By.CSS_SELECTOR, '.average-user-rating')
                        user_rating = int(user_rating_elem.get_attribute('class').split()[1].split('-')[2])
                        flag = True
                    except IndexError:
                        print(json.dumps({'url': url, 'id': movie_id, 'error': 'index'}))
                    except ValueError:
                        print(json.dumps({'url': url, 'id': movie_id, 'error': 'int cast'}))
                    except:
                        user_count = 0
                        user_rating = None
                        flag = True

                    if flag:
                        file.write(json.dumps({'id': movie_id, 'user_count': user_count, 'user_rating': user_rating}) + '\n')
                time.sleep(3)
        driver.quit()
except FileNotFoundError:
    print('data.jsonl not found')