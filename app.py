from flask import Flask, request, render_template_string
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

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    back_questions = soup.find_all(class_='back question')

    answers = [q.get_text(strip=True) for q in back_questions]

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
