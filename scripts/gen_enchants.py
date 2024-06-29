# Read data/enchants.json and generate the enchantments
# To a mkdocs compatible format

import json
import os

# Example enchantment
# {
#     "appliesTo": "Элитры",
#     "highestLevel": 5,
#     "description": "Шанс отравить противника и обретение регенерации.",
#     "display": "Приговор"
# }
groupToNames = {
    "SIMPLE": "Обычный",
    "UNIQUE": "Редкий",
    "ELITE": "Элитный",
    "ULTIMATE": "Высший",
    "LEGENDARY": "Легендарный",
    "FABLED": "Мифический",
}


def main():
    with open("data/enchants.json", encoding="utf-8") as f:
        data = json.load(f)
    md_string = ""
    # the keys are group ids, values are enchantments
    for group in groupToNames.keys():
        group_name = groupToNames[group]
        md_string += f"=== \"{group_name}\""
        enchantment_string = "\n"
        for enchantment in data[group]:
            enchantment_string += f"    !!! enchants-{group.lower()} \"{enchantment['display']}\"\n"
            enchantment_string += f"        {enchantment['description']}<br><br>"
            enchantment_string += f"**Применяется к:** {enchantment['appliesTo']}<br>"
            enchantment_string += f"**Максимальный уровень:** {enchantment['highestLevel']}\n"
        md_string += enchantment_string

    with open("../docs/enchantments.md", "w", encoding="utf-8") as f:
        f.write(md_string)


main()
