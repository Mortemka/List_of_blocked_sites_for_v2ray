import requests
import json

# URL для загрузки файла доменов
url = "https://raw.githubusercontent.com/dartraiden/no-russia-hosts/master/hosts.txt"
response = requests.get(url)

if response.status_code == 200:
    content = response.text

    # Обработка строк: убираем комментарии и пустые строки
    lines = content.splitlines()
    processed_domains = ["domain:" + line.strip() for line in lines if line.strip() and not line.startswith("#")]

    # Читаем существующий JSON файл
    custom_json_filename = "v2ray_custom.json"
    try:
        with open(custom_json_filename, "r") as file:
            v2ray_config = json.load(file)
    except FileNotFoundError:
        # Если файл не найден, создаем новую структуру
        v2ray_config = []

    # Создаем новый блок с кастомными доменами
    new_rule = {
        "type": "field",
        "port": "",
        "outboundTag": "proxy",  # или "proxy", в зависимости от ваших нужд
        "domain": processed_domains
    }

    # Добавляем новый блок в конфигурацию
    v2ray_config.append(new_rule)

    # Сохраняем обновленный JSON файл
    with open(custom_json_filename, "w") as file:
        json.dump(v2ray_config, file, indent=4)

    print(f"Файл '{custom_json_filename}' успешно обновлен и сохранен.")
else:
    print("Ошибка при загрузке файла.")
