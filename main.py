import os
import sys
import shutil
import time
import json
import tempfile
import zipfile
from pathlib import Path

# Для Windows
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except:
        pass
    import msvcrt
else:
    import termios
    import tty

# Конфигурация GitHub
GITHUB_REPO = "JohnnySiinsss/minecraft-bedrock-crack"  # Замените на ваш репозиторий
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
GITHUB_RELEASE_URL = f"https://github.com/{GITHUB_REPO}/releases/latest"
CRACK_FILES_ZIP = "minecraft_crack.zip"
LOCAL_VERSION_FILE = "version.txt"

# Цвета ANSI
class Colors:
    PURPLE = '\033[95m'
    LIGHT_PURPLE = '\033[38;5;141m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_color(text, color=Colors.WHITE):
    print(f"{color}{text}{Colors.RESET}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print_color("""
╔═══════════════════════════════════════════════════════╗
║     ██╗ ██████╗ ██╗  ██╗███╗   ██╗███╗   ██╗██╗   ██╗║
║     ██║██╔═══██╗██║  ██║████╗  ██║████╗  ██║╚██╗ ██╔╝║
║     ██║██║   ██║███████║██╔██╗ ██║██╔██╗ ██║ ╚████╔╝ ║
║██   ██║██║   ██║██╔══██║██║╚██╗██║██║╚██╗██║  ╚██╔╝  ║
║╚█████╔╝╚██████╔╝██║  ██║██║ ╚████║██║ ╚████║   ██║   ║
║ ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝   ╚═╝   ║
║                                                       ║
║      ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗ ║
║     ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ║
║     ██║     ██████╔╝███████║██║     █████╔╝ █████╗   ║
║     ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝   ║
║     ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗ ║
║      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ║
║                                                       ║
║         [•] MINECRAFT BEDROCK CRACK v3.0             ║
║         [•] АВТО-ОБНОВЛЕНИЕ + ПРЯМАЯ УСТАНОВКА      ║
╚═══════════════════════════════════════════════════════╝
""", Colors.PURPLE)
    
    print_color("═" * 60, Colors.PURPLE)
    print_color("\n⚠  ДАННАЯ ПРОГРАММА НУЖНА ДЛЯ КРАКА MINECRAFT ВЫШЕ 1.21.100", Colors.YELLOW)
print_color("⚠  ВСЕ ФАЙЛЫ УСТАНАВЛИВАЮТСЯ АВТОМАТИЧЕСКИ", Colors.YELLOW)
    print_color("═" * 60 + "\n", Colors.PURPLE)

def wait_key():
    """Ожидание нажатия клавиши"""
    print_color("\n[Нажмите Enter для продолжения...]", Colors.LIGHT_PURPLE)
    if sys.platform == "win32":
        try:
            msvcrt.getch()
        except:
            input()
    else:
        input()

def check_internet():
    """Проверка интернет-соединения"""
    import socket
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False

def get_latest_version():
    """Получение последней версии с GitHub"""
    try:
        import urllib.request
        
        headers = {'User-Agent': 'Minecraft-Crack-Updater'}
        req = urllib.request.Request(GITHUB_API_URL, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if 'tag_name' in data:
                version = data['tag_name'].lstrip('v')
                
                # Ищем архив с файлами крака
                for asset in data.get('assets', []):
                    if asset.get('name') == CRACK_FILES_ZIP:
                        return {
                            'version': version,
                            'download_url': asset['browser_download_url'],
                            'size': asset.get('size', 0)
                        }
                
                # Если нашли любой архив
                for asset in data.get('assets', []):
                    if asset.get('name', '').endswith('.zip'):
                        return {
                            'version': version,
                            'download_url': asset['browser_download_url'],
                            'size': asset.get('size', 0)
                        }
                        
    except Exception:
        return None
    
    return None

def get_current_version():
    """Получение текущей версии"""
    if os.path.exists(LOCAL_VERSION_FILE):
        try:
            with open(LOCAL_VERSION_FILE, 'r') as f:
                return f.read().strip()
        except:
            pass
    return "1.0.0"

def save_current_version(version):
    """Сохранение текущей версии"""
    try:
        with open(LOCAL_VERSION_FILE, 'w') as f:
            f.write(version)
    except:
        pass

def download_with_progress(url, dest_path):
    """Загрузка файла с прогресс-баром"""
    try:
        import urllib.request
        
        headers = {'User-Agent': 'Minecraft-Crack-Updater'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded = 0
            
            with open(dest_path, 'wb') as f:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    
                    f.write(buffer)
                    downloaded += len(buffer)
                    
                    if total_size > 0:
                        percent = min(100, (downloaded / total_size) * 100)
                        bar_length = 40
                        filled_length = int(bar_length * downloaded // total_size)
                        bar = '█' * filled_length + '░' * (bar_length - filled_length)
                        sys.stdout.write(f'\r[•] Загрузка: [{bar}] {percent:.1f}%')
                        sys.stdout.flush()
            
            print()
            return True
            
    except Exception:
        return False

def extract_to_minecraft(zip_path, minecraft_folder):
    """Распаковка архива прямо в папку Minecraft"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Получаем список файлов
            file_list = zip_ref.namelist()
            
            # Счетчик скопированных файлов
            copied = 0
            
            for file in file_list:
                # Извлекаем файл
                zip_ref.extract(file, minecraft_folder)
                
                # Полный путь к извлеченному файлу
                extracted_path = os.path.join(minecraft_folder, file)
                
                # Если это файл (а не папка)
                if os.path.isfile(extracted_path):
                    # Проверяем нужные ли это файлы
                    filename = os.path.basename(file)
                    if filename in ['winmm.dll', 'OnlineFix64.dll', 'OnlineFix.ini', 'dlllist.txt']:
                        # Если файл был в подпапке, перемещаем его в корень
                        if os.path.dirname(file):
                            target_path = os.path.join(minecraft_folder, filename)
                            if extracted_path != target_path:
                                shutil.move(extracted_path, target_path)
                                extracted_path = target_path
                        
                        print_color(f"[✓] Установлен: {filename}", Colors.GREEN)
                        copied += 1
            
            if copied > 0:
                print_color(f"[✓] Установлено файлов: {copied}", Colors.GREEN)
                return True
            else:
                print_color("[!] В архиве не найдены файлы крака", Colors.RED)
                return False
                
    except Exception as e:
        print_color(f"[!] Ошибка распаковки: {e}", Colors.RED)
        return False

def find_minecraft_folder():
    """Автоматический поиск папки Minecraft"""
    print_color("\n[•] Ищу Minecraft на компьютере...", Colors.LIGHT_PURPLE)
    
    # Список возможных путей
    search_paths = [
        # Xbox App версия
        r"C:\XboxGames\Minecraft for Windows\Content",
        r"C:\Program Files\ModifiableWindowsApps\Minecraft",
        
        # Microsoft Store версия
        os.path.expandvars(r"%LOCALAPPDATA%\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe"),
        os.path.expandvars(r"%PROGRAMFILES%\WindowsApps\Microsoft.MinecraftUWP_8wekyb3d8bbwe"),
        
        # Альтернативные пути
        os.path.expanduser(r"~\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe"),
        r"D:\Games\Minecraft",
        r"E:\Games\Minecraft",
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            print_color(f"[✓] Найдена папка Minecraft: {path}", Colors.GREEN)
            return path
    
    # Если не нашли автоматически, пробуем ручной поиск
    print_color("[!] Автоматический поиск не удался", Colors.YELLOW)
    
    # Пробуем найти через реестр (для Windows)
    if sys.platform == "win32":
        try:
            import winreg
            
            # Пробуем найти в реестре
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Minecraft.exe")
                minecraft_exe, _ = winreg.QueryValueEx(key, "")
                minecraft_folder = os.path.dirname(minecraft_exe)
                if os.path.exists(minecraft_folder):
                    print_color(f"[✓] Найдено через реестр: {minecraft_folder}", Colors.GREEN)
                    return minecraft_folder
            except:
                pass
        except:
            pass
    
    return None

def get_minecraft_version(folder):
    """Получение версии Minecraft из папки"""
    try:
        # Пробуем найти файл с версией
        version_files = [
            os.path.join(folder, "version.txt"),
            os.path.join(folder, "appxmanifest.xml"),
            os.path.join(folder, "Minecraft.Windows.exe"),
        ]
        
        for file in version_files:
            if os.path.exists(file):
                if file.endswith("appxmanifest.xml"):
                    # Читаем XML и ищем версию
                    import xml.etree.ElementTree as ET
                    tree = ET.parse(file)
                    root = tree.getroot()
                    
                    # Ищем версию в тегах
                    for elem in root.iter():
                        if 'Version' in elem.attrib:
                            return elem.attrib['Version']
                
                elif file.endswith("Minecraft.Windows.exe"):
                    # Пробуем получить версию EXE файла
                    try:
                        if sys.platform == "win32":
                            import win32api
                            info = win32api.GetFileVersionInfo(file, "\\")
                            version = "%d.%d.%d.%d" % (info['FileVersionMS'] / 65536,
                                                      info['FileVersionMS'] % 65536,
                                                      info['FileVersionLS'] / 65536,
                                                      info['FileVersionLS'] % 65536)
                            return version.split('.')[0:3]  # Берем только первые три части
                    except:
                        pass
        
        # Если не нашли, возвращаем дефолтную версию
        return "1.21.100"
        
    except:
        return "1.21.100"

def check_update():
    """Проверка обновлений"""
    print_color("\n[•] Проверяю обновления...", Colors.LIGHT_PURPLE)
    
    if not check_internet():
        print_color("[✓] Работаю в оффлайн режиме", Colors.GREEN)
        return True
    
    latest = get_latest_version()
    if not latest:
        print_color("[✓] Не удалось проверить обновления, использую локальные файлы", Colors.YELLOW)
        return True
    
    current_version = get_current_version()
    
    if latest['version'] == current_version:
        return True
    
    print_color(f"[!] Доступна новая версия: v{latest['version']}", Colors.YELLOW)
    print_color("[?] Обновить? (да/нет): ", Colors.LIGHT_PURPLE)
    
    if input().strip().lower() in ['да', 'д', 'yes', 'y']:
        return download_and_update()
    
    return True

def download_and_update():
    """Скачивание и установка обновления"""
    print_color("\n[•] Загружаю обновление...", Colors.LIGHT_PURPLE)
    
    latest = get_latest_version()
    if not latest:
        return False
    
    temp_dir = tempfile.mkdtemp(prefix="mc_crack_")
    zip_path = os.path.join(temp_dir, CRACK_FILES_ZIP)
    
    if download_with_progress(latest['download_url'], zip_path):
        print_color("[✓] Обновление загружено", Colors.GREEN)
        
        # Обновляем локальные файлы
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('.')
            
            save_current_version(latest['version'])
            print_color("[✓] Программа обновлена", Colors.GREEN)
            
            # Очищаем временные файлы
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            print_color("\n[!] Перезапустите программу", Colors.YELLOW)
            wait_key()
            sys.exit(0)
            
        except Exception as e:
            print_color(f"[!] Ошибка обновления: {e}", Colors.RED)
            return False
    
    return False

def install_crack():
    """Основная функция установки крака"""
    print_color("\n" + "═" * 60, Colors.PURPLE)
    print_color("[•] ЗАПУСК ПРОЦЕССА УСТАНОВКИ КРАКА", Colors.LIGHT_PURPLE)
    print_color("═" * 60, Colors.PURPLE)
    
    # 1. Проверка обновлений
    if not check_update():
        print_color("[!] Проблема с обновлениями, продолжаю...", Colors.YELLOW)
    
    # 2. Поиск Minecraft
    print_color("\n[•] Поиск Minecraft...", Colors.LIGHT_PURPLE)
    minecraft_folder = find_minecraft_folder()
    
    if not minecraft_folder:
        print_color("[!] Minecraft не найден!", Colors.RED)
        print_color("\n[i] Установите Minecraft из Microsoft Store или Xbox App", Colors.CYAN)
        print_color("[i] Или укажите путь вручную:", Colors.CYAN)
        print_color("[?] Введите путь к папке Minecraft: ", Colors.LIGHT_PURPLE)
        
        minecraft_folder = input().strip()
        if not os.path.exists(minecraft_folder):
            print_color("[!] Папка не существует!", Colors.RED)
            wait_key()
            return False
    
    print_color(f"[✓] Папка Minecraft: {minecraft_folder}", Colors.GREEN)
    
    # 3. Проверка версии Minecraft
    mc_version = get_minecraft_version(minecraft_folder)
    print_color(f"[✓] Версия Minecraft: {mc_version}", Colors.GREEN)
    
    # 4. Проверка интернета для загрузки файлов
    if not check_internet():
        print_color("[!] Нет интернет-соединения!", Colors.RED)
        print_color("[!] Файлы крака не могут быть загружены", Colors.RED)
        wait_key()
        return False
    
    # 5. Загрузка файлов крака
    print_color("\n[•] Получение файлов крака...", Colors.LIGHT_PURPLE)
    
    latest = get_latest_version()
    if not latest:
        print_color("[!] Не удалось получить файлы", Colors.RED)
        wait_key()
        return False
    
    print_color(f"[i] Используется версия крака: v{latest['version']}", Colors.CYAN)
    
    temp_dir = tempfile.mkdtemp(prefix="mc_crack_")
    zip_path = os.path.join(temp_dir, CRACK_FILES_ZIP)
    
    print_color("[•] Загрузка файлов...", Colors.LIGHT_PURPLE)
    if not download_with_progress(latest['download_url'], zip_path):
        print_color("[!] Ошибка загрузки", Colors.RED)
        shutil.rmtree(temp_dir, ignore_errors=True)
        wait_key()
        return False
    
    # 6. Установка файлов
    print_color("\n[•] Установка файлов...", Colors.LIGHT_PURPLE)
    
    # Создаем бекап оригинальных файлов
    backup_folder = os.path.join(minecraft_folder, "backup_original")
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    
    # Файлы для бекапа
    original_files = ['winmm.dll', 'OnlineFix64.dll']
    for file in original_files:
        src = os.path.join(minecraft_folder, file)
        if os.path.exists(src):
            dst = os.path.join(backup_folder, file)
            shutil.copy2(src, dst)
            print_color(f"[✓] Бекап {file}", Colors.GREEN)
    
    # Извлекаем файлы крака
    if extract_to_minecraft(zip_path, minecraft_folder):
        print_color("[✓] Файлы крака установлены", Colors.GREEN)
    else:
        # Альтернативный метод: вручную копируем файлы
        print_color("[!] Авто-установка не удалась, пробую вручную...", Colors.YELLOW)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Ищем нужные файлы в архиве
                for file in zip_ref.namelist():
                    if file.endswith(('winmm.dll', 'OnlineFix64.dll', 'OnlineFix.ini', 'dlllist.txt')):
                        # Извлекаем файл
                        zip_ref.extract(file, temp_dir)
                        temp_file = os.path.join(temp_dir, file)
                        
                        # Копируем в Minecraft
                        dest_file = os.path.join(minecraft_folder, os.path.basename(file))
                        shutil.copy2(temp_file, dest_file)
                        print_color(f"[✓] Установлен {os.path.basename(file)}", Colors.GREEN)
        except:
            print_color("[!] Критическая ошибка установки", Colors.RED)
            shutil.rmtree(temp_dir, ignore_errors=True)
            wait_key()
            return False
    
    # 7. Очистка
    shutil.rmtree(temp_dir, ignore_errors=True)
    save_current_version(latest['version'])
    
    # 8. Завершение
    print_color("\n" + "═" * 60, Colors.PURPLE)
    print_color("[✓] КРАК УСПЕШНО УСТАНОВЛЕН!", Colors.GREEN)
    print_color("═" * 60, Colors.PURPLE)
    
    print_color(f"\n📁 Папка Minecraft: {minecraft_folder}", Colors.CYAN)
    print_color(f"📁 Бекап файлов: {backup_folder}", Colors.CYAN)
    print_color(f"🔧 Версия крака: v{latest['version']}", Colors.CYAN)
    
    print_color("\n⚠ ВАЖНЫЕ ШАГИ ПОСЛЕ УСТАНОВКИ:", Colors.YELLOW)
    print_color("1. Добавьте папку Minecraft в исключения антивируса", Colors.YELLOW)
    print_color("2. Перезапустите компьютер", Colors.YELLOW)
    print_color("3. Запускайте Minecraft через ярлык", Colors.YELLOW)
    
    print_color("\n[i] Если игра не запускается:", Colors.CYAN)
    print_color("• Проверьте исключения в антивирусе", Colors.CYAN)
    print_color("• Переустановите крак", Colors.CYAN)
    print_color("• Обратитесь в Telegram: https://t.me/JohnnySiinsss", Colors.CYAN)
    
    return True

def show_info():
    clear_screen()
    print_header()
    print_color("""
📋 ИНФОРМАЦИЯ О ПРОГРАММЕ v3.0:

✨ ОСОБЕННОСТИ:
• Полностью автоматическая установка
• Авто-поиск Minecraft на компьютере
• Скачивание актуальных файлов крака
• Создание бекапов оригинальных файлов
• Проверка обновлений

🔧 ПРОЦЕСС РАБОТЫ:
1. Программа ищет Minecraft автоматически
2. Скачивает свежие файлы крака
3. Создает бекап оригинальных файлов
4. Устанавливает файлы крака
5. Все происходит автоматически!

⚠ ВАЖНО:
• Антивирус может блокировать файлы крака
• Добавьте папку Minecraft в исключения
• Интернет обязателен для загрузки файлов
• Бекапы сохраняются в папке backup_original
""", Colors.LIGHT_PURPLE)
    wait_key()

def show_contact():
    clear_screen()
    print_header()
    print_color(f"""
📞 СВЯЗЬ С СОЗДАТЕЛЕМ:

Telegram: https://t.me/JohnnySiinsss
GitHub: https://github.com/{GITHUB_REPO}

⚠ ПОДДЕРЖКА:
• Сообщайте о проблемах с установкой
• Предлагайте улучшения
• Следите за обновлениями

🔧 ТЕХНИЧЕСКАЯ ИНФОРМАЦИЯ:
• Файлы крака скачиваются автоматически
• Не требуются ручные действия
• Все файлы проверяются на актуальность
""", Colors.LIGHT_PURPLE)
    wait_key()

def cleanup():
    """Очистка временных файлов"""
    import glob
    temp_patterns = [
        "mc_crack_*",
        "temp_*",
        "*.tmp",
        "*.temp"
    ]
    
    for pattern in temp_patterns:
        for file in glob.glob(pattern):
            try:
                if os.path.isdir(file):
                    shutil.rmtree(file, ignore_errors=True)
                else:
                    os.remove(file)
            except:
                pass

def main_menu():
    while True:
        try:
            print_header()
            print_color(f"[i] Текущая версия: v{get_current_version()}", Colors.CYAN)
            
            print_color("\n[1] Установить крак (автоматически)", Colors.LIGHT_PURPLE)
            print_color("[2] Проверить обновления", Colors.LIGHT_PURPLE)
            print_color("[3] Информация о программе", Colors.LIGHT_PURPLE)
            print_color("[4] Связь с создателем", Colors.LIGHT_PURPLE)
            print_color("[5] Выход", Colors.LIGHT_PURPLE)
            
            print_color("\n[?] Выберите действие (1-5): ", Colors.LIGHT_PURPLE)
            choice = input().strip()
            
            if choice == "1":
                if install_crack():
                    print_color("\n[✓] Процесс завершен успешно!", Colors.GREEN)
                else:
                    print_color("\n[!] Установка не удалась", Colors.RED)
                wait_key()
            elif choice == "2":
                if check_update():
                    print_color("\n[✓] Обновлений не найдено", Colors.GREEN)
                wait_key()
            elif choice == "3":
                show_info()
            elif choice == "4":
                show_contact()
            elif choice == "5":
                print_color("\n[•] Выход...", Colors.LIGHT_PURPLE)
                cleanup()
                break
            else:
                print_color("[!] Неверный выбор!", Colors.RED)
                time.sleep(1)
                
        except KeyboardInterrupt:
            print_color("\n\n[!] Выход...", Colors.RED)
            cleanup()
            break
        except Exception as e:
            print_color(f"\n[!] Ошибка: {str(e)[:100]}", Colors.RED)
            time.sleep(2)

def main():
    """Главная функция"""
    try:
        # Очистка перед запуском
        cleanup()
        
        # Создаем файл версии если его нет
        if not os.path.exists(LOCAL_VERSION_FILE):
            save_current_version("1.0.0")
        
        # Запускаем меню
        main_menu()
        
    except Exception as e:
        print_color(f"\n[!] Критическая ошибка: {e}", Colors.RED)
        cleanup()
    
    print_color("\n\n[Нажмите Enter для выхода...]", Colors.LIGHT_PURPLE)
    input()

if __name__ == "__main__":
    main()
