import sqlite3
import time
from functools import wraps
import datetime

def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[DECORATOR] {func.__name__} — {end - start:.4f} soniya")
        return result
    return wrapper

class TodoList:
    def __init__(self, user_name="Foydalanuvchi"):
        self._user_name = user_name
        self._create_db()

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, value):
        if len(value.strip()) < 2:
            raise ValueError("Ism kamida 2 harfdan iborat bo'lishi kerak!")
        self._user_name = value
        print(f"Foydalanuvchi nomi yangilandi: {value}")

    def _create_db(self):
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            priority TEXT,
            created_at TEXT,
            completed_at TEXT
        )''')
        conn.commit()
        conn.close()

    @timer_decorator
    def add_task(self, title, priority="Medium"):
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO tasks (title, priority, created_at) VALUES (?, ?, ?)",
                       (title, priority, now))
        conn.commit()
        conn.close()
        print(f"✅ Vazifa qo'shildi: {title} (Prioritet: {priority})")

    @timer_decorator
    def complete_task(self, task_id):
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("UPDATE tasks SET status='Completed', completed_at=? WHERE id=?", (now, task_id))
        conn.commit()
        conn.close()
        print(f"✅ {task_id}-raqamli vazifa bajarildi!")

    @timer_decorator
    def show_tasks(self, status=None):
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        if status:
            cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY id", (status,))
        else:
            cursor.execute("SELECT * FROM tasks ORDER BY id")
        tasks = cursor.fetchall()
        conn.close()
        print(f"\n=== {self.user_name} ning Vazifalari ===")
        if not tasks:
            print("Hozircha vazifalar yo'q.")
            return
        for t in tasks:
            print(f"ID:{t[0]:<3} | {t[1]:<40} | Holat: {t[2]:<10} | Prioritet: {t[3]}")

    def info(self):
        print(f"\n📋 Foydalanuvchi: {self.user_name}")

if __name__ == "__main__":
    todo = TodoList()
    print("=== Todo List (Vazifalar Ro'yxati) ===")
    while True:
        print("\n1. Vazifa qo'shish\n2. Vazifani bajarilgan deb belgilash\n3. Barcha vazifalarni ko'rish\n4. Faqat bajarilmaganlarni ko'rish\n5. Foydalanuvchi nomini o'zgartirish\n6. Chiqish")
        choice = input("Tanlang (1-6): ").strip()
        if choice == "1":
            title = input("Vazifa nomi: ").strip()
            priority = input("Prioritet (Low/Medium/High): ").strip() or "Medium"
            todo.add_task(title, priority)
        elif choice == "2":
            try:
                tid = int(input("Vazifa ID raqami: "))
                todo.complete_task(tid)
            except ValueError:
                print("ID raqam bo'lishi kerak!")
        elif choice == "3":
            todo.show_tasks()
        elif choice == "4":
            todo.show_tasks("Pending")
        elif choice == "5":
            new_name = input("Yangi ism: ").strip()
            try:
                todo.user_name = new_name
            except ValueError as e:
                print(e)
        elif choice == "6":
            print("Dastur tugadi!")
            break
        else:
            print("Noto'g'ri tanlov!")
