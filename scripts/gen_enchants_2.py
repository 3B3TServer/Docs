# Что бы использовать этот скрипт:
# 1. Поместите данные зачарований в файл `data/enchantments.yml`
# 2. Установите библиотеку: pip install PyYAML
# 3. Запустите этот скрипт

try:
    import yaml
    print("✅ PyYAML успешно импортирован")
except ImportError:
    print("❌ Ошибка: PyYAML не установлен!")
    print("Установите его командой: pip install PyYAML")
    input("Нажмите Enter для выхода...")
    exit(1)

import os

# Mapping групп на русские названия
groupToNames = {
    "SIMPLE": "Обычный",
    "UNIQUE": "Редкий", 
    "ELITE": "Элитный",
    "ULTIMATE": "Высший",
    "LEGENDARY": "Легендарный",
    "FABLED": "Мифический",
    "REDQUEST": "Квестовый",
    "COSMIC": "Космический",
}


def get_highest_level(levels_dict):
    """Получить максимальный уровень из словаря levels"""
    if not levels_dict or not isinstance(levels_dict, dict):
        return 1
    
    max_level = 0
    for level_key in levels_dict.keys():
        try:
            level_num = int(level_key)
            max_level = max(max_level, level_num)
        except ValueError:
            continue
    
    return max_level if max_level > 0 else 1


def clean_display_name(display):
    """Очистить название от цветовых кодов"""
    if not display:
        return ""
    
    # Удаляем %group-color% и другие плейсхолдеры
    display = display.replace('%group-color%', '')
    
    # Можно добавить удаление других цветовых кодов если нужно
    # display = re.sub(r'&[0-9a-fk-or]', '', display)
    
    return display.strip()


def main():
    # Проверяем существование директории data
    if not os.path.exists("data"):
        print("Ошибка: директория 'data' не найдена!")
        return
    
    print("Читаем файл data/enchantments.yml...")
    try:
        with open("data/enchantments.yml", "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print("Ошибка: файл data/enchantments.yml не найден!")
        return
    except yaml.YAMLError as e:
        print(f"Ошибка при чтении YAML файла: {e}")
        return
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла: {e}")
        return
    
    if not data:
        print("Ошибка: файл пуст или содержит неверные данные!")
        return
    
    if not isinstance(data, dict):
        print("Ошибка: корневой элемент должен быть словарем (объектом)!")
        return
    
    print(f"Загружено {len(data)} зачарований из файла")
    print(f"Первые 3 ключа: {list(data.keys())[:3]}")
    
    # Проверяем структуру первого зачарования
    first_key = list(data.keys())[0]
    first_enchant = data[first_key]
    print(f"Структура первого зачарования '{first_key}': {list(first_enchant.keys()) if isinstance(first_enchant, dict) else 'НЕ СЛОВАРЬ'}")
    
    # Группируем зачарования по группам
    grouped_enchants = {}
    processed_count = 0
    
    print("Обрабатываем зачарования...")
    for enchant_id, enchant_data in data.items():
        print(f"Обрабатываем: {enchant_id}")
        
        if not isinstance(enchant_data, dict):
            print(f"  ❌ Данные зачарования '{enchant_id}' должны быть словарем")
            continue
        
        # Получаем группу зачарования
        group = enchant_data.get('group')
        print(f"  Группа: {group}")
        
        if not group:
            print(f"  ❌ У зачарования '{enchant_id}' отсутствует группа")
            continue
        
        # Проверяем, есть ли группа в словаре названий
        if group not in groupToNames:
            print(f"  ❌ Неизвестная группа '{group}' для зачарования '{enchant_id}' - пропускаем")
            continue
        
        # Проверяем наличие необходимых полей
        required_fields = ['display', 'description', 'applies-to']
        missing_fields = [field for field in required_fields if field not in enchant_data]
        
        if missing_fields:
            print(f"  ❌ У зачарования '{enchant_id}' отсутствуют поля {missing_fields}")
            continue
        
        # Проверяем, что поля не пустые
        empty_fields = [field for field in required_fields if not str(enchant_data[field]).strip()]
        if empty_fields:
            print(f"  ❌ У зачарования '{enchant_id}' есть пустые поля: {empty_fields}")
            continue
        
        # Получаем максимальный уровень
        highest_level = get_highest_level(enchant_data.get('levels', {}))
        print(f"  Максимальный уровень: {highest_level}")
        
        # Очищаем название от цветовых кодов
        clean_display = clean_display_name(enchant_data['display'])
        print(f"  Очищенное название: '{clean_display}'")
        
        # Создаем объект зачарования
        enchant_obj = {
            'display': clean_display,
            'description': enchant_data['description'],
            'appliesTo': enchant_data['applies-to'],
            'highestLevel': highest_level,
            'id': enchant_id
        }
        
        # Добавляем в группу
        if group not in grouped_enchants:
            grouped_enchants[group] = []
        grouped_enchants[group].append(enchant_obj)
        processed_count += 1
        print(f"  ✅ Успешно обработано")
    
    print(f"\nУспешно обработано {processed_count} зачарований")
    print(f"Группы найдены: {list(grouped_enchants.keys())}")
    
    if not grouped_enchants:
        print("❌ Ни одно зачарование не было обработано! Проверьте структуру файла.")
        return
    
    # Генерируем Markdown
    md_string = "[//]: # (generated by scripts/gen_enchants.py)\n\n"
    
    # Проходим по группам в порядке, определенном в groupToNames
    for group in groupToNames.keys():
        if group not in grouped_enchants:
            continue
        
        group_name = groupToNames[group]
        md_string += f"=== \"{group_name}\"\n"
        
        # Сортируем зачарования по названию
        enchantments = sorted(grouped_enchants[group], key=lambda x: x['display'])
        
        for enchantment in enchantments:
            md_string += f"    !!! enchants-{group.lower()} \"{enchantment['display']}\"\n"
            md_string += f"        {enchantment['description']}<br><br>\n"
            md_string += f"        **Применяется к:** {enchantment['appliesTo']}<br>\n"
            md_string += f"        **Максимальный уровень:** {enchantment['highestLevel']}\n\n"
    
    # Проверяем существование директории docs
    docs_dir = "../docs"
    if not os.path.exists(docs_dir):
        print(f"Предупреждение: директория '{docs_dir}' не существует, создаем...")
        try:
            os.makedirs(docs_dir)
        except Exception as e:
            print(f"Ошибка при создании директории: {e}")
            return

    try:
        with open("../docs/enchantments.md", "w", encoding="utf-8") as f:
            f.write(md_string)
        print("Файл документации успешно создан: ../docs/enchantments.md")
        print(f"Обработано групп: {len(grouped_enchants)}")
        total_enchants = sum(len(enchants) for enchants in grouped_enchants.values())
        print(f"Всего зачарований: {total_enchants}")
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")
        return


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
    
    # Пауза чтобы увидеть результат
    input("\nНажмите Enter для выхода...")