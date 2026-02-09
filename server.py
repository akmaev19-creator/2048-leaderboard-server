from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Разрешаем запросы из браузера

# Файл для хранения рекордов
RECORDS_FILE = 'records.json'

# Загружаем рекорды из файла
def load_records():
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

# Сохраняем рекорды в файл
def save_records(records):
    with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# Главная страница для проверки
@app.route('/')
def home():
    return '✅ Сервер для игры 2048 работает!'

# Получить топ-10 рекордов (GET запрос)
@app.route('/api/top', methods=['GET'])
def get_top_records():
    records = load_records()
    # Сортируем по убыванию счета и берем первые 10
    top = sorted(records, key=lambda x: x['score'], reverse=True)[:10]
    return jsonify(top)

# Сохранить новый рекорд (POST запрос)
@app.route('/api/save', methods=['POST'])
def save_record():
    try:
        # Получаем данные из запроса
        data = request.json
        user_id = str(data.get('userId', '0'))
        username = data.get('username', 'Аноним').strip() or 'Аноним'
        score = int(data.get('score', 0))

        # Загружаем текущие рекорды
        records = load_records()

        # Ищем запись этого пользователя
        user_record = None
        for record in records:
            if str(record.get('userId')) == user_id:
                user_record = record
                break

        if user_record:
            # Обновляем, если новый счет больше
            if score > user_record['score']:
                user_record['score'] = score
                user_record['username'] = username
                user_record['date'] = datetime.now().isoformat()
        else:
            # Добавляем новую запись
            records.append({
                'userId': user_id,
                'username': username,
                'score': score,
                'date': datetime.now().isoformat()
            })

        # Сохраняем обновленный список
        save_records(records)

        return jsonify({'success': True, 'message': 'Рекорд сохранен'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
