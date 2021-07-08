# Dsa

## Опис

Цей репозиторій містить код для опрацювання протоколів автоматизованого розподілу
судових справ між суддями, що [публікуються](https://dsa.court.gov.ua/dsa/inshe/oddata/757) від 25.06.2021 Державною судовою адміністрацією України. 

* зчитує бінарний вміст поля DOC_HTML (zip архів)
* відкриває html файл, що лежить у zip архівові
* витягує meta поля та їхній вміст з html файлу
* оновлює документ (його копію)  


## Встановлення

Відтворення віртуального середовища:

```bash
$ git clone https://github.com/hp0404/dsa.git
$ cd dsa
$ python3 -m venv env
$ . env/bin/activate
```

Встановлення залежностей та самої бібліотеки:
```bash
(env)$ pip install -r requirements.txt 
(env)$ pip install -e .
```


## Використання

```python
from dsa import Documents

# поки тестую на одному файлі
docs = Documents.from_json(
    "../data/20210507000000_20210508000000.json",
    normalize_values=True
)
docs.process_documents()

# оригінальні дані, перший документ
print(docs.raw_data[0])

# опрацьовані дані, перший документ
print(docs.processed_data[0])

# збереження як json
docs.save(json_file="test.json")

# збереження як jsonl
docs.save(jsonl_file="test.jsonl")
```