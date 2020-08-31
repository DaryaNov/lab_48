from webapp.forms import SimpleSearchForm
from webapp.models import Basket


def search_form(request):
    form = SimpleSearchForm(request.GET)
    return {'search_form': form}


def basket(request):
    return {'basket': Basket(request)}