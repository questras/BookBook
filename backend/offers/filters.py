from django_filters.rest_framework import FilterSet, DateTimeFromToRangeFilter, CharFilter, DateTimeFromToRangeFilter;

from .models import Offer


class OfferSearchFilter(FilterSet):
    title = CharFilter(method='filter_search')
    author = CharFilter(method='filter_trigram')
    state = CharFilter(method='filter_trigram')
    city = CharFilter(method='filter_trigram')
    created = DateTimeFromToRangeFilter()
    updated = DateTimeFromToRangeFilter()

    def filter_search(self, qs, name, value):
        k = '{}__search'.format(name)
        return qs.filter(**{k: value})

    def filter_trigram(self,  qs, name, value):
        k = '{}__trigram_similar'.format(name)
        return qs.filter(**{k: value})

    class Meta:
        model = Offer
        fields = ('title', 'author', 'state', 'city', 'updated', 'created')
