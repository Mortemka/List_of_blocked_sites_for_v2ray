import sqlite3
import json
import random
import string
import subprocess
import argparse

def generate_unique_id(length=19):
    """Генерирует уникальный идентификатор из случайных цифр."""
    return ''.join(random.choices(string.digits, k=length))

def load_rule_set(file_path):
    """Загружает ruleSet из указанного JSON файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            rule_set = json.load(file)
            return rule_set
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при загрузке ruleSet: {e}")
        return None

def insert_new_routing_item(db_path, remarks_name, rule_set):
    """Вставляет новый элемент в таблицу RoutingItem."""
    unique_id = generate_unique_id()
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получаем количество строк в таблице для вычисления значения sort
        cursor.execute("SELECT COUNT(*) FROM RoutingItem")
        row_count = cursor.fetchone()[0]
        sort_value = row_count + 1

        # Создание нового элемента с параметрами enabled, locked и sort
        cursor.execute("""
            INSERT INTO RoutingItem (id, remarks, ruleSet, enabled, locked, sort)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (unique_id, remarks_name, json.dumps(rule_set), 1, 0, sort_value))
        
        conn.commit()
        print(f"Новый элемент добавлен в базу данных с id: {unique_id}")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        if conn:
            conn.close()

def main(remarks_name, db_path, ruleset_file_path, ip_url, domain_url):
    # Загрузка данных ruleSet
    rule_set = load_rule_set(ruleset_file_path)
    
    if rule_set:
        # Вставка нового элемента в базу данных
        insert_new_routing_item(db_path, remarks_name, rule_set)
        
        # Запуск скриптов для обновления базы данных с передачей аргументов
        try:
            # Обновление базы данных с доменами
            subprocess.run([
                "python", "update_database_with_domains.py", 
                "--remarks_name", remarks_name, 
                "--db_path", db_path, 
                "--url", domain_url
            ], check=True)
            
            # Обновление базы данных с IP
            subprocess.run([
                "python", "update_database_with_ips.py", 
                "--remarks_name", remarks_name, 
                "--db_path", db_path, 
                "--url", ip_url
            ], check=True)

            print("База данных успешно обновлена доменами и IP.")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении скрипта: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Создание нового RoutingItem и обновление базы данных.")
    parser.add_argument("--remarks_name", type=str, required=True, help="Имя списка для нового элемента")
    parser.add_argument("--db_path", type=str, required=True, help="Путь к базе данных")
    parser.add_argument("--ruleset_file_path", type=str, required=True, help="Путь к файлу с данными ruleSet")
    parser.add_argument("--ip_url", type=str, required=True, help="URL для скачивания списка IP-адресов")
    parser.add_argument("--domain_url", type=str, required=True, help="URL для скачивания списка доменов")
    
    args = parser.parse_args()
    main(args.remarks_name, args.db_path, args.ruleset_file_path, args.ip_url, args.domain_url)
