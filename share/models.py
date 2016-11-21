from __future__ import unicode_literals

from django.contrib.auth.models import User as authuser
from django.db import models


BEERSIZES = (
    (0, 'Can'),
    (1, 'Bottle, glass'),
    (2, 'Bottle, plastic')
)

LIST_TYPES = (
    (0, 'Collab'),
    (1, 'Tasting'),
)


class ShareUser(models.Model):
    user = models.OneToOneField(authuser)
    get_notifications = models.BooleanField(default=True)

    def __unicode__(self):
        return u'{0}'.format(self.user.username)


class Currency(models.Model):
    name = models.CharField(max_length=3)
    exchange_rate = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        help_text=u'Exchange rate against SEK, '
                  u'ie: if 1DKK = 1.30SEK, supplied value should be 1.3'
    )
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{0} {1} ({2})'.format(
            self.name,
            self.exchange_rate,
            self.created_at.strftime('%H:%I:%S %d/%m-%Y')
        )


class Site(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    logo = models.ImageField(blank=True, null=True, name=u'Logotype')
    currency = models.ForeignKey(Currency)

    def __unicode__(self):
        return u'{0}'.format(
            self.name,
        )


class Brewery(models.Model):
    name = models.CharField(max_length=255)
    logo_thumb = models.ImageField(blank=True, null=True, name=u'Logotype, thumbnail')
    logo_big = models.ImageField(blank=True, null=True, name=u'Logotype, Large')

    def __unicode__(self):
        return u'{0}'.format(self.name)


class BeerSize(models.Model):
    volume = models.IntegerField(
        help_text=u'Volume in centiliters'
    )
    container = models.IntegerField(
        choices=BEERSIZES
    )
    approx_weight = models.IntegerField(
        null=True, blank=True,
        help_text=u'weight in grams'
    )

    def __unicode__(self):
        return u'{0} cl. {1}'.format(self.volume, BEERSIZES[self.container][1])


class BeerStyle(models.Model):
    name = models.CharField(max_length=127)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class AbstractBaseBeer(models.Model):
    name = models.CharField(max_length=255)
    thumb = models.ImageField(blank=True, null=True, name=u'Thumbnail')
    image = models.ImageField(blank=True, null=True, name=u'Image')
    style = models.ForeignKey(BeerStyle)
    brewery = models.ForeignKey(Brewery, related_name=u'beers')
    collabs = models.ManyToManyField(
        Brewery, related_name=u'collab_beers',
        null=True, blank=True
    )

    def __unicode__(self):
        return u'{0} - {1}'.format(self.name, self.brewery.name)


class Beer(models.Model):
    base_beer = models.ForeignKey(AbstractBaseBeer)
    year = models.IntegerField(blank=True, null=True)
    abv = models.DecimalField(decimal_places=2, max_digits=4)
    ean = models.IntegerField(blank=True, null=True)
    site = models.ForeignKey(Site)
    price = models.DecimalField(
        decimal_places=2, max_digits=5,
        help_text=u'Use price in currency used by the site.'
    )
    size = models.ForeignKey(BeerSize)
    bulk_only = models.BooleanField(
        default=False,
        help_text=u'Only sold in multipacks'
    )
    bulk_size = models.IntegerField(
        null=True, blank=True,
        help_text=u'Multipack limit'
    )

    def get_sek_price(self):
        return self.price * self.site.currency.exchange_rate

    def __unicode__(self):
        return u'{0} {1}% {2}. {3} {4} SEK'.format(
            self.base_beer, self.abv,
            self.size, self.site, self.price*self.site.currency.exchange_rate
        )


class ShippingCosts(models.Model):
    site = models.ForeignKey(Site)
    weight = models.IntegerField(
        blank=True, null=True
    )
    free_shipping_limit = models.IntegerField(
        blank=True, null=True,
    )


class ListBeer(models.Model):
    beer = models.ForeignKey(Beer)
    qty = models.IntegerField(
        null=True, blank=True,
        help_text=u'Use this to limit the number of times a beer can be claimed.'
                  u'Not needed @ tasting-lists'
    )

    def get_full_price(self):
        if self.qty:
            return self.qty * self.beer.get_sek_price()
        else:
            return u'No quantity specified'

    def get_actual_price(self):
        price = 0
        for b in self.beerlistbeer_set.all():
            price += b.get_sek_price()
        return price

    def get_original_price(self):
        price = 0
        for b in self.beerlistbeer_set.all():
            price += b.get_original_price()
        return price

    def get_total_claimed(self):
        claimed = 0
        for beercount in self.beerlistbeer_set.all():
            claimed += beercount.qty
        return claimed

    def get_total_grams(self):
        grams = 0
        for blb in self.beerlistbeer_set.all():
            grams += blb.listbeer.beer.size.approx_weight
        return grams

    def __unicode__(self):
        return u'{0} ({1})'.format(self.beer, self.qty)


class BeerList(models.Model):
    name = models.CharField(max_length=255)
    info = models.TextField(
        null=True, blank=True,
        help_text=u'Describe your intentions with the list'
    )
    type = models.IntegerField(choices=LIST_TYPES)
    is_active = models.BooleanField()
    admins = models.ManyToManyField(
        ShareUser, related_name=u'BeerListAdmin',
        help_text=u'Admins are allowed to invite new users, and add/remove beers from list'
    )
    users = models.ManyToManyField(
        ShareUser, related_name=u'beerlistuser',
        blank=True, null=True,
        help_text=u'Users are only allowed to claim beers from the list'
    )
    beers = models.ManyToManyField(ListBeer)

    def get_total_per_beer(self):
        all_beers = self.beers.all()
        beer_dict = {}
        for beer in all_beers:
            beer_dict[beer] = []

    def get_total_price(self):
        price = 0
        for listbeer in self.beers.all():
            price += listbeer.get_actual_price()
        return price

    def get_total_claimed(self):
        claimed = 0
        for listbeer in self.beers.all():
            claimed += listbeer.get_total_claimed()
        return claimed

    def get_total_weight(self):
        grams = 0
        for listbeer in self.beers.all():
            grams += listbeer.get_total_grams()
        return grams

    def get_total_per_site(self):
        sites = {}
        for listbeer in self.beers.all():
            try:
                sites[listbeer.beer.site].append(listbeer.get_original_price())
            except KeyError:
                sites[listbeer.beer.site] = [listbeer.get_original_price()]
        return sites

    def __unicode__(self):
        return u'{0}'.format(self.name)


class BeerListBeer(models.Model):
    listbeer = models.ForeignKey(ListBeer)
    qty = models.IntegerField(
        default=1,
        help_text=u'Number of this beer claimed by user.'
                  u'Can not be greater than ListBeer qty.'
                  u'Only needed at collab-lists'
        )
    user = models.ForeignKey(
        ShareUser,
        null=True, blank=True,
        help_text=u'Only needed at collab-lists'
    )

    def get_nice_format(self):
        return(
            self.user.user.username,
            self.qty,
            self.get_sek_cost_string()
        )

    def get_sek_price(self):
        beer = self.listbeer.beer
        convert = beer.price * beer.site.currency.exchange_rate
        price = convert * self.qty
        return price

    def get_original_price(self):
        beer = self.listbeer.beer
        price = beer.price * self.qty
        return price

    def get_sek_cost_string(self):
        return u'{0} SEK'.format(self.get_sek_price())


class Message(models.Model):
    author = models.ForeignKey(ShareUser, related_name=u'written_messages')
    written_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    to_user = models.ForeignKey(ShareUser, related_name=u'user_messages')
    to_list = models.ForeignKey(BeerList)
    read_by = models.ManyToManyField(
        ShareUser,
        null=True, blank=True,
        help_text=u'Users in list who has read the message.'
    )