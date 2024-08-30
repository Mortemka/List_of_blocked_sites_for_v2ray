import sqlite3
import json

# Путь к базе данных
DB_PATH = r"E:\Soft\Helpfull\v2rayN-With-Core\guiConfigs\guiNDB.db"
# Имя списка для поиска
REMARKS_NAME = "Whitelist"

def extract_rule_set_from_database(db_path, remarks_name):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Получаем данные из таблицы по имени списка (remarks)
        cursor.execute("SELECT ruleSet FROM RoutingItem WHERE remarks=?", (remarks_name,))
        row = cursor.fetchone()
        
        if row:
            # Если запись найдена, загружаем ruleSet
            rule_set = json.loads(row[0])
            return rule_set
        else:
            print("Запись не найдена.")
            return None
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return None
    finally:
        if conn:
            conn.close()

def save_rule_set_to_file(rule_set, remarks_name):
    file_name = f"BASE_{remarks_name}.json"
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(rule_set, file, indent=4, ensure_ascii=False)
        print(f"Данные успешно сохранены в файл '{file_name}'.")
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")

def main():
    # Извлечение данных ruleSet из базы данных
    rule_set = extract_rule_set_from_database(DB_PATH, REMARKS_NAME)
    
    if rule_set is not None:
        # Сохранение данных в файл
        save_rule_set_to_file(rule_set, REMARKS_NAME)

if __name__ == "__main__":
    main()
