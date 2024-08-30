import subprocess
import os

# Путь к базе данных (относительный)
DB_PATH = r"E:\Soft\Helpfull\v2rayN-With-Core\guiConfigs\guiNDB.db"

# Настройки для "White List"
REMARKS_NAME_WHITE = "White List"
RULESET_FILE_PATH_WHITE = "BASE_Whitelist.json"

# Настройки для "Black List"
REMARKS_NAME_BLACK = "Black List"
RULESET_FILE_PATH_BLACK = "BASE_black_list.json"

# URL для скачивания списка IP-адресов и доменов (пока одинаковые для обоих списков)
IP_URL = "https://github.com/sanmai/blacklist/raw/master/blacklist.txt"
DOMAIN_URL = "https://raw.githubusercontent.com/dartraiden/no-russia-hosts/master/hosts.txt"

def run_insert_script(remarks_name, db_path, ruleset_file_path, ip_url, domain_url):
    """Запуск скрипта insert_new_routing_item.py с передачей аргументов."""
    try:
        subprocess.run([
            "python", "insert_new_routing_item.py",
            "--remarks_name", remarks_name,
            "--db_path", db_path,
            "--ruleset_file_path", ruleset_file_path,
            "--ip_url", ip_url,
            "--domain_url", domain_url
        ], check=True)
        print(f"Список '{remarks_name}' успешно добавлен в базу данных.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при добавлении списка '{remarks_name}': {e}")

def main():
    # Добавление "White List"
    run_insert_script(REMARKS_NAME_WHITE, DB_PATH, RULESET_FILE_PATH_WHITE, IP_URL, DOMAIN_URL)
    
    # Добавление "Black List"
    run_insert_script(REMARKS_NAME_BLACK, DB_PATH, RULESET_FILE_PATH_BLACK, IP_URL, DOMAIN_URL)

if __name__ == "__main__":
    main()
