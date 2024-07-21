from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>Rule 34 Jeopardy</h1>
        <form action="/scrape" method="post">
            <label for="game_id">Game ID:</label>
            <input type="text" id="game_id" name="game_id">
            <button type="submit">Grab</button>
        </form>
    '''

@app.route('/scrape', methods=['POST'])
def scrape():
    jeopardy_id = request.form['game_id']
    url = f'https://jeopardylabs.com/play/{jeopardy_id}'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    driver.find_element(By.ID, "submit").click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    back_questions = soup.find_all(class_='back question')

    answers = [q.get_text(strip=True) for q in back_questions]

    driver.quit()

    num_columns = 5
    columns = [[] for _ in range(num_columns)]

    for i, answer in enumerate(answers):
        columns[i % num_columns].append(answer)

    return render_template_string('''
        <h1>Jeopardy Antworten</h1>
        <div style="display: flex;">
            {% for column in columns %}
                <ul style="margin-right: 20px;">
                    {% for answer in column %}
                        <li>{{ answer }}</li>
                    {% endfor %}
                </ul>
            {% endfor %}
        </div>
        <a href="/">Zurück zur Startseite</a>
    ''', columns=columns)

if __name__ == '__main__':
    app.run(debug=True)
