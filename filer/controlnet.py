import os

from .base import FilerGroupBase
from .util import FileSize


class FilerGroupControlNet(FilerGroupBase):
    name = 'controlnet'

    @classmethod
    def _get_list(cls, dir):
        rs = []
        unit = 'GB'
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                # if not filename.endswith('.pth') :
                #     continue

                r = {}
                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])
                r['size'] = FileSize().get_filesize(r['filepath'], unit)

                rs.append(r)

        return rs
