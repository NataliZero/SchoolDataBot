import sqlite3
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, DATABASE_PATH

# Настраиваем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Определяем состояния для сбора данных
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Функция для сохранения данных в базу
def save_to_db(name, age, grade):
    conn = None  # Инициализируем переменную conn
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (name, age, grade) VALUES (?, ?, ?)
        ''', (name, age, grade))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
    finally:
        if conn:
            conn.close()

# Хендлер для команды /start
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    # Очищаем состояние, если пользователь начал заново
    await state.clear()
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

# Хендлер для получения имени
@dp.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

# Хендлер для получения возраста
@dp.message(Form.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуй снова.")
        return
    await state.update_data(age=int(message.text))
    await message.answer("В каком ты классе?")
    await state.set_state(Form.grade)

# Хендлер для получения класса и сохранения данных
@dp.message(Form.grade)
async def get_grade(message: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['name']
    age = user_data['age']
    grade = message.text

    # Сохраняем данные в базу
    save_to_db(name, age, grade)

    await message.answer(f"Спасибо! Мы сохранили твои данные:\nИмя: {name}\nВозраст: {age}\nКласс: {grade}")

    # Сбрасываем состояние пользователя
    await state.clear()

# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
