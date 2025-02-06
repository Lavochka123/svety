# app.py
from flask import Flask, render_template, request, jsonify
import telegram  # библиотека для работы с Telegram Bot API

app = Flask(__name__, template_folder='template')  # убедитесь, что папка называется "templates"

# Ваш токен Telegram‑бота (тот же, что используется в bot.py)
TELEGRAM_BOT_TOKEN = "8046219766:AAGFsWXIFTEPe8aaTBimVyWm2au2f-uIYSs"
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

@app.route('/invite/<invite_id>')
def invite(invite_id):
    # Получаем параметры из query-параметров
    design = request.args.get('design', 'design_elegant')
    intro = request.args.get('intro', 'Привет! Я подготовил для тебя нечто особенное...')
    proposal = request.args.get('proposal', 'Давай проведём этот вечер вместе. Я знаю уютное место!')
    chat_id = request.args.get('chat_id', None)

    # Если варианты времени передаются не динамически, можно задать их здесь (иначе можно передать через URL)
    times = request.args.getlist('times') or ['🕗 19:00 | 21 января', '🌙 20:30 | 22 января', '☕ 17:00 | 23 января']

    invite_data = {
        'design': design,
        'intro': intro,
        'proposal': proposal,
        'times': times,
        'chat_id': chat_id
    }
    return render_template('invite.html', data=invite_data)

@app.route('/choose_time', methods=['GET', 'POST'])
def choose_time():
    if request.method == 'GET':
        design = request.args.get('design', 'design_elegant')
        intro = request.args.get('intro', 'Привет! Я подготовил для тебя нечто особенное...')
        proposal = request.args.get('proposal', 'Давай проведём этот вечер вместе. Я знаю уютное место!')
        chat_id = request.args.get('chat_id', None)
        times = ['🕗 19:00 | 21 января', '🌙 20:30 | 22 января', '☕ 17:00 | 23 января']
        return render_template('choose_time.html', design=design, intro=intro, proposal=proposal, times=times,
                               chat_id=chat_id)
    else:
        # Обработка POST-запроса с выбранным временем
        selected_time = request.form.get('selected_time')
        design = request.form.get('design')
        intro = request.form.get('intro')
        proposal = request.form.get('proposal')
        chat_id = request.form.get('chat_id')  # chat_id мужчины, переданный из предыдущей страницы

        # Отправляем уведомление в Telegram мужчине
        if chat_id:
            message = (f"Отличные новости!\n"
                       f"Девушка выбрала время для встречи:\n{selected_time}")
            try:
                bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                print("Ошибка при отправке сообщения в Telegram:", e)

        return render_template('confirmation.html', design=design, intro=intro, proposal=proposal,
                               selected_time=selected_time)

# Новый эндпоинт для получения ответа от девушки через AJAX или POST-запрос со страницы приглашения
@app.route('/response', methods=['POST'])
def response():
    # Ожидаем JSON-данные: chat_id, response (например, "Извини, не могу" или выбранное время)
    data = request.get_json()
    chat_id = data.get('chat_id')
    response_text = data.get('response')
    selected_time = data.get('selected_time', '')

    message = f"Девушка ответила: {response_text}"
    if selected_time:
        message += f"\nВыбранное время: {selected_time}"

    try:
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print("Ошибка при отправке ответа в Telegram:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True)
