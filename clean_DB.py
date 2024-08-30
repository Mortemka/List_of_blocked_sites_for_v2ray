import sqlite3

# Путь к базе данных
DB_PATH = r"E:\Soft\Helpfull\v2rayN-With-Core\guiConfigs\guiNDB.db"

def clear_routing_item_table(db_path):
    """Очищает таблицу RoutingItem, удаляя все записи."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Удаление всех записей из таблицы RoutingItem
        cursor.execute("DELETE FROM RoutingItem")

        conn.commit()
        print("Таблица RoutingItem успешно очищена.")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        if conn:
            conn.close()

def main():
    clear_routing_item_table(DB_PATH)

if __name__ == "__main__":
    main()
