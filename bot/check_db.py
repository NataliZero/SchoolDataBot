import os
import sqlite3

# Абсолютный путь к файлу базы данных
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../database/school_data.db")

# Подключение к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создание таблицы students (если её нет)
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL
)
''')

# Выполнение запроса для просмотра данных
cursor.execute("SELECT * FROM students;")
rows = cursor.fetchall()

# Вывод данных в консоль
print("Сохраненные записи:")
for row in rows:
    print(row)

# Закрытие подключения
conn.commit()
conn.close()
