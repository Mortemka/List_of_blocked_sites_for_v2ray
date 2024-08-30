import os
import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import zipfile
import json

# Ссылка на файл с серверами
servers_url = "https://dd3baaf4.withblancvpn.online/s/1658806413714649999cb744aa8ccabe"
# Репозиторий с конфигурациями
config_repo_url = "https://github.com/Mortemka/List_of_blocked_sites_for_v2ray/archive/refs/heads/main.zip"

# Функция загрузки серверов
def download_servers():
    response = requests.get(servers_url)
    response.raise_for_status()
    return response.text.splitlines()

# Функция загрузки конфигураций из репозитория
def download_configs():
    response = requests.get(config_repo_url)
    response.raise_for_status()
    with open("config_repo.zip", "wb") as f:
        f.write(response.content)
    with zipfile.ZipFile("config_repo.zip", "r") as zip_ref:
        zip_ref.extractall("config_repo")
    os.remove("config_repo.zip")
    configs_path = "config_repo/List_of_blocked_sites_for_v2ray-main/configs"
    return [os.path.join(configs_path, f) for f in os.listdir(configs_path) if f.endswith(".json")]

# Функция запуска Xray
def start_vpn(server, config):
    try:
        with open(config, 'r') as f:
            config_data = json.load(f)
        # Пример замены адреса и порта сервера в конфигурации
        config_data['outbounds'][0]['settings']['vnext'][0]['address'] = server.split(':')[0]
        config_data['outbounds'][0]['settings']['vnext'][0]['port'] = int(server.split(':')[1])

        # Запись измененной конфигурации
        with open("temp_config.json", "w") as f:
            json.dump(config_data, f, indent=4)
        
        # Запуск Xray
        os.system(f"xray -config temp_config.json")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# Создание GUI
def create_gui(servers, configs):
    root = tk.Tk()
    root.title("VPN Manager")

    # Список серверов
    tk.Label(root, text="Доступные серверы:").pack()
    server_listbox = tk.Listbox(root, width=50, height=10)
    server_listbox.pack()
    for server in servers:
        server_listbox.insert(tk.END, server)

    # Список конфигураций
    tk.Label(root, text="Доступные конфигурации:").pack()
    config_listbox = tk.Listbox(root, width=50, height=10)
    config_listbox.pack()
    for config in configs:
        config_listbox.insert(tk.END, os.path.basename(config))

    # Кнопка запуска
    def on_start():
        selected_server = server_listbox.get(tk.ACTIVE)
        selected_config = config_listbox.get(tk.ACTIVE)
        if selected_server and selected_config:
            start_vpn(selected_server, configs[config_listbox.curselection()[0]])
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите сервер и конфигурацию")

    tk.Button(root, text="Старт", command=on_start).pack()

    root.mainloop()

# Основной код
try:
    servers = download_servers()
    configs = download_configs()
    create_gui(servers, configs)
except Exception as e:
    messagebox.showerror("Ошибка", str(e))
