import os

from .base import FilerGroupBase
from .util import FileSize


class FilerGroupCheckpoints(FilerGroupBase):
    name = 'checkpoints'

    @classmethod
    #* ファイル拡張子の制限や sha256 の機能などが一律で不要のままであればスーパークラスへ移管できそう
    def _get_list(cls, dir):
        rs = []
        unit = 'GB'
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                # if not filename.endswith('.ckpt') and not filename.endswith('.safetensors') and not filename.endswith('.vae.pt'):
                #     continue

                r = {}
                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])
                r['size'] = FileSize().get_filesize(r['filepath'], unit)

                rs.append(r)

        return rs
