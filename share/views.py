from django.shortcuts import render, render_to_response

from share.models import BeerList, LIST_TYPES, BeerListBeer


def index(request):
    return render_to_response('index.html', locals())


def profile(request):
    user = request.user.shareuser
    admin_lists = BeerList.objects.filter(admins=user)
    user_lists = BeerList.objects.filter(users=user)
    return render_to_response('profile.html', locals())


def beerlistview(request, list_id):
    list = BeerList.objects.get(pk=list_id)
    total_claimed = list.get_total_claimed()
    total_price = list.get_total_price()
    total_weight = list.get_total_weight()
    rules = list.get_total_per_site()

    print rules
    if list.get_type_display() == 'Collab':
        claimed = BeerListBeer.objects.filter(listbeer__beerlist=list)
        claimed_beers = {}
        for beer in claimed:
            try:
                claimed_beers[beer.listbeer].append(
                    beer.get_nice_format()
                )
            except KeyError:
                claimed_beers[beer.listbeer] = [
                    beer.get_nice_format()
                ]

        return render_to_response('beerlist_collab.html', locals())
