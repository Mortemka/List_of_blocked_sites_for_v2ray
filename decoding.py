import geoip2.database
import struct

# Путь к вашей базе данных GeoLite2-Country
geoip_database_path = 'GeoLite2-Country.mmdb'

# Выходной файл geoip.dat
output_file_path = 'geoip_ru.dat'

def create_geoip_dat():
    # Открываем базу данных
    reader = geoip2.database.Reader(geoip_database_path)
    
    # Открываем файл geoip.dat для записи в бинарном формате
    with open(output_file_path, 'wb') as output_file:
        # Записываем заголовок (например, 4 байта для meta информации)
        output_file.write(struct.pack('>I', 0))  # Примерный заголовок

        # Инициализация для хранения информации
        ip_ranges = []

        # Перебираем все возможные IP-адреса (например, в диапазоне 0.0.0.0 - 255.255.255.255)
        for ip in range(0, 2**32):
            ip_str = f"{(ip >> 24) & 0xFF}.{(ip >> 16) & 0xFF}.{(ip >> 8) & 0xFF}.{ip & 0xFF}"
            try:
                response = reader.country(ip_str)
                # Проверяем, является ли страна "RU"
                if response.country.iso_code == 'RU':
                    # Если да, то добавляем запись в массив
                    ip_ranges.append(ip)
            except geoip2.errors.AddressNotFoundError:
                continue  # Адрес не найден, продолжаем

        # Записываем IP-адреса в файл
        for ip in ip_ranges:
            ip_prefix = struct.pack('>I', ip)
            country_code = struct.pack('B', 1)  # Укажите правильный код страны
            output_file.write(ip_prefix + country_code)

    reader.close()

create_geoip_dat()
print("geoip.dat файл успешно создан.")
