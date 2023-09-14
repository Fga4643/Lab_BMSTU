from django.shortcuts import render

from spares.utils.db import *


def index(request):
    query = request.GET.get("spares")
    spares = searchSpares(query) if query else getSpares()

    context = {
        "spares": spares,
        "search_query": query if query else ""
    }

    return render(request, "home_page.html", context)


def spareOrderPage(request, spare_id):
    spare = getSpareById(spare_id)

    context = {
        "username": "Админ",
        "spare_id": spare_id,
        "spare_name": spare["spare_name"],
        "spare_description": spare["spare_description"],
        "spare_price": spare["spare_price"],
        "spare_condition": spare["spare_condition"]
    }

    return render(request, "order_page.html", context)
