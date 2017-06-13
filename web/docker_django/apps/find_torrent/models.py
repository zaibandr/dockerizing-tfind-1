from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.


class Torrent(models.Model):
    title = models.TextField(max_length=600, db_index=True)
    orig_title = models.TextField(default='', null=True, max_length=800)
    magnet = models.TextField(max_length=1200, db_index=True)
    provider_url = models.TextField(max_length=600)
    provider = models.CharField(max_length=200, default='Extratorrent.cc', editable=False, db_index=True)

    t_hash = models.CharField(max_length=40, null=True, db_index=True)
    file_list = models.TextField(null=True)

    peers = models.IntegerField(null=True, db_index=True)
    seeds = models.IntegerField(null=True, db_index=True)
    complete = models.IntegerField(null=True, db_index=True)
    tr_list = JSONField(db_index=True, null=True)

    # last_check = models.DateTimeField(null=True, db_index=True)
    name_pars = JSONField(db_index=True, null=True)

    # t_file = models.FileField(upload_to=TORRENT_ROOT, null=True)
    # last_scrape_peer = models.DateField(null=True)

    class Meta:
        unique_together = ('magnet', 'provider_url',)

    def __str__(self):
        return "{}\t({})".format(self.title, self.provider)


class Trend(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)
    last_check = models.DateTimeField(null=True, db_index=True)
    count_check = models.IntegerField(null=True, db_index=True)
    priority = models.IntegerField(null=True, db_index=True)

    def __str__(self):
        return '{}\t({})'.format(self.title, self.last_check)


if __name__ == '__main__':
    print('main')