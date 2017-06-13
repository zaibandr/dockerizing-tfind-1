from haystack import indexes
from .models import Torrent


class TorrentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    provider = indexes.CharField(model_attr='provider')
    magnet = indexes.CharField(model_attr='magnet')
    provider_url = indexes.CharField(model_attr='provider_url')

    peers = indexes.IntegerField(model_attr='peers')
    seeds = indexes.IntegerField(model_attr='seeds')
    complete = indexes.IntegerField(model_attr='complete')
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='title')

    suggestions = indexes.FacetCharField()

    def prepare(self, obj):
        prepared_data = super(TorrentIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def get_model(self):
        return Torrent

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all().order_by('title')
