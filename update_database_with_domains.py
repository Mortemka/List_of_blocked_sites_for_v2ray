import requests
import sqlite3
import json
import argparse

def download_domain_list(url):
    try:
        # Загрузка списка доменов
        response = requests.get(url)
        response.raise_for_status()
        content = response.text

        # Обработка строк: убираем комментарии и пустые строки
        lines = content.splitlines()
        processed_domains = ["domain:" + line.strip() for line in lines if line.strip() and not line.startswith("#")]

        return processed_domains
    except requests.exceptions.RequestException as e:
        print(f"Ошибка загрузки доменов: {e}")
        return []

def update_database_with_domains(db_path, domain_list, remarks_name):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Создание нового правила с доменами
        new_rule = {
            "id": "new-rule-id",  # ID для нового правила, можно оставить пустым или уникальным
            "outboundTag": "proxy",
            "domain": domain_list,
            "enabled": True
        }
        
        # Получаем текущие данные из таблицы по имени списка (remarks)
        cursor.execute("SELECT ruleSet FROM RoutingItem WHERE remarks=?", (remarks_name,))
        row = cursor.fetchone()
        
        if row:
            # Если запись найдена, загружаем и обновляем
            rule_set = json.loads(row[0])
        else:
            # Если запись не найдена, создаем новый список правил
            rule_set = []
        
        # Добавляем новое правило
        rule_set.append(new_rule)
        
        # Обновляем запись в базе данных
        cursor.execute(
            "UPDATE RoutingItem SET ruleSet=? WHERE remarks=?", 
            (json.dumps(rule_set), remarks_name)
        )
        
        # Если записи с таким remarks нет, создаем новую
        if cursor.rowcount == 0:
            cursor.execute(
                "INSERT INTO RoutingItem (remarks, ruleSet) VALUES (?, ?)",
                (remarks_name, json.dumps(rule_set))
            )
        
        conn.commit()
        print("База данных успешно обновлена.")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
    finally:
        if conn:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description="Обновление базы данных с доменами.")
    parser.add_argument("--remarks_name", required=True, help="Имя списка для поиска.")
    parser.add_argument("--db_path", required=True, help="Путь к базе данных.")
    parser.add_argument("--url", required=True, help="URL для загрузки файла доменов.")
    
    args = parser.parse_args()
    
    # Загрузка доменов
    domain_list = download_domain_list(args.url)
    
    if domain_list:
        # Обновление базы данных
        update_database_with_domains(args.db_path, domain_list, args.remarks_name)

if __name__ == "__main__":
    main()
