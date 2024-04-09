import os

from .base import FilerGroupBase


class FilerGroupOther(FilerGroupBase):
    name = 'other'

    @classmethod
    def _get_list(cls, dir):
        rs = []
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                r = {}
                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])
                r['size'] = cls.get_filesize_kilobytes(r['filepath'])

                rs.append(r)

        return rs
