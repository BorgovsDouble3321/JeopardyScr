from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        
        <style>
            body {
                background-color: black;
                color: white;
                font-family: Arial, sans-serif;
            }
        </style>
    
        <h1>Rule 34 Jeopardy</h1>
        <form action="/scrape" method="post">
            <label for="game_id">Game ID:</label>
            <input type="text" id="game_id" name="game_id">
            <input type="number" id="columns_amount" name="columns_amount" min="1" max="15" step="1" placeholder="0">
            <button type="submit">Grab</button>
        </form>
    '''

@app.route('/scrape', methods=['POST'])
def scrape():
    jeopardy_id = request.form['game_id']
    columns_amount = request.form['columns_amount']
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
        <style>
            body {
                background-color: black;
                color: white;
                font-family: Arial, sans-serif;
            }
            h1 {
                text-align: center;
            }
            .columns {
                display: flex;
                justify-content: center;
            }
            ul {
                list-style-type: disc;
                padding: 0;
                margin: 0 20px;
            }
            li::marker {
                color: white;
            }
            a {
                color: white;
                display: block;
                text-align: center;
                margin-top: 20px;
            }
        </style>
        <h1>Jeopardy Antworten</h1>
        <div class="columns">
            {% for column in columns %}
                <ul>
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
