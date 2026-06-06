from django.contrib import admin

from .models import Offer, OfferDetail, OfferDetailFeature

# Register your models here.
admin.site.register(Offer)
admin.site.register(OfferDetail)
admin.site.register(OfferDetailFeature)
