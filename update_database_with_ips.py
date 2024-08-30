import argparse
import requests
import sqlite3
import json

def download_ip_list(url):
    try:
        # Загрузка списка IP-адресов
        response = requests.get(url)
        response.raise_for_status()
        ip_list = response.text.splitlines()
        # Отфильтруем пустые строки
        ip_list = [ip.strip() for ip in ip_list if ip.strip()]
        return ip_list
    except requests.exceptions.RequestException as e:
        print(f"Ошибка загрузки IP-адресов: {e}")
        return []

def update_database_with_ips(db_path, remarks_name, ip_list):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Создание нового правила с IP-адресами
        new_rule = {
            "id": "new-rule-id",  # ID для нового правила, можно оставить пустым или уникальным
            "outboundTag": "proxy",
            "ip": ip_list,
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
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description="Обновление базы данных с IP-адресами.")
    parser.add_argument('--db_path', required=True, help="Путь к базе данных.")
    parser.add_argument('--url', required=True, help="URL для загрузки списка IP-адресов.")
    parser.add_argument('--remarks_name', required=True, help="Имя списка для поиска в базе данных.")

    args = parser.parse_args()

    # Загрузка IP-адресов
    ip_list = download_ip_list(args.url)
    
    if ip_list:
        # Обновление базы данных
        update_database_with_ips(args.db_path, args.remarks_name, ip_list)

if __name__ == "__main__":
    main()
