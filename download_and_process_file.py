import requests

def download_and_process_file(url):
    try:
        # Шаг 1: Загрузка файла
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешности запроса

        # Шаг 2: Обработка содержимого файла
        # Предположим, что данные в файле зашифрованы в base64
        raw_data = response.text
        
        # Если данные не зашифрованы, это можно пропустить
        import base64
        decoded_data = base64.b64decode(raw_data).decode('utf-8', errors='ignore')
        
        # Разделение строк по пробелам, если в оригинале они не разделены
        vpn_links = decoded_data.split()

        # Шаг 3: Запись обработанных данных в новый файл
        with open('decoded_vpn_links.txt', 'w', encoding='utf-8') as file:
            for link in vpn_links:
                file.write(link + '\n')
        
        print("Обработка завершена. Данные сохранены в 'decoded_vpn_links.txt'.")
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка загрузки файла: {e}")
    except Exception as e:
        print(f"Произошла ошибка обработки: {e}")


# Вызов функции с ссылкой на файл
download_and_process_file('https://dd3baaf4.withblancvpn.online/s/1658806413714649999cb744aa8ccabe')
