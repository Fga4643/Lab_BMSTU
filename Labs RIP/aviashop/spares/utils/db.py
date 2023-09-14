db = {
    "spares": [
        {
            "spare_id": 1,
            "spare_name": "Насос ЭЦН-109а с электродвигателем ГЭА-6А",
            "spare_description": """Новые! Упаковки, коробки, паспорта, ярлыки консервации, хранение - сухой склад!

 6шт. цена за шт.

 За опт - скидка!""",
            "spare_price": 25000,
            "spare_condition": "Новое"
        },
        {
            "spare_id": 2,
            "spare_name": "Двигатель РУ 19-300",
            "spare_description": """После ремонта. ППР- 0 ч.

Без формуляра. С официальным происхождением.

Турбореактивный двигатель РУ 19-300 предназначен для установки на самолете в качестве дополнительной энергоустановки.""",
            "spare_price": 500000,
            "spare_condition": "Б/у"
        },
        {
            "spare_id": 3,
            "spare_name": "Кабина самолета Boeing 737",
            "spare_description": """Подойдет для реализации проектов: авиатренажер, авиасимулятор, развлекательный аттракцион, или любой другой.

Boeing 737 — узкофюзеляжный ближне-среднемагистральный пассажирский самолёт.""",
            "spare_price": 1000000,
            "spare_condition": "Б/у"
        },
        {
            "spare_id": 4,
            "spare_name": "Авиационные колёса",
            "spare_description": "",
            "spare_price": 200000,
            "spare_condition": "Б/у"
        },
        {
            "spare_id": 5,
            "spare_name": "Авиагоризонт АГБ-2",
            "spare_description": "Новый, с хранения, пломбы целые. Картонная упаковка и паспорт утрачены в процессе хранения.",
            "spare_price": 12000,
            "spare_condition": "Новое"
        },
        {
            "spare_id": 6,
            "spare_name": "Регулятор Р68-ДК",
            "spare_description": "Состояние на фото. Агрегат новый с хранения. Заводская упаковка утрачена вместе с документами на агрегат. Консервация регулятора заводская, повторной не подвергался.",
            "spare_price": 600000,
            "spare_condition": "Новое"
        }
    ]
}


def getSpares():
    return db["spares"]


def getSpareById(spare_id):
    for spare in db["spares"]:
        if spare["spare_id"] == spare_id:
            return spare


def searchSpares(spare_name):
    spares = getSpares()

    res = []

    for spare in spares:
        if spare_name.lower() in spare["spare_name"].lower():
            res.append(spare)

    return res
