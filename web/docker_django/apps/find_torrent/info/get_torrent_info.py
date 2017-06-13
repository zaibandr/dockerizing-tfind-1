from torrentool.api import Torrent


# Reading and modifying an existing file.

my_torrent = Torrent.from_file('q.torrent')
magnet = 'magnet:?xt=urn:btih:7c041bed5d3fd77dd1148333432e6f5091baff18&dn=Bon+Jovi+-+Long+Way+From+Home+%5Blive-rock%5D+1993+%28MP3-320%29+-+%5B%3DFaith%3D%5D&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Fglotorrents.pw%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fzer0day.to%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce'


def size_readable(size):
    d = {
        1073741824: 'GiB',
        1048576: 'MiB',
        1024: 'KiB',
        1: 'B',
    }

    for i in sorted(d.keys(), reverse=True):
        if size >= i:
            s = '{} {}'.format(round(size/i, 2), d[i])
            return s

for file in my_torrent.files:
    file_name, size = file
    print(file_name, size_readable(size))
