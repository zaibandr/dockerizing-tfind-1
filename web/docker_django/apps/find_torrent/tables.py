import django_tables2 as tables
from django.utils.html import format_html
from .models import Torrent


class MagnetColumn(tables.Column):
    def render(self, value):
        link_title = "Download this torrent using magnet"
        img_src = "https://s3-eu-west-1.amazonaws.com/zaibandr/magnet.png"
        return format_html('<a href="{}"><img src="{}" alt="M" title="{}"></a>', str(value), img_src, link_title)


class ProviderColumn(tables.Column):
    def render(self, value, record):
        return format_html('<a href="{}"><p class="text-center">{}</p></a>', record['provider_url'], value)


class TorrentTable(tables.Table):
    magnet = MagnetColumn(verbose_name='M', orderable=False)
    provider = ProviderColumn(orderable=False)

    class Meta:
        model = Torrent

        # add class="paleblue" to <table> tag
        fields = ('title', 'peers', 'seeds', 'complete', 'provider', 'magnet')