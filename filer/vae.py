import os

from .base import FilerGroupBase


class FilerGroupVAE(FilerGroupBase):
    name = 'vae'

    @classmethod
    def _get_list(cls, dir):
        rs = []
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                # if not filename.endswith('.pt') and not filename.endswith('.ckpt') and not filename.endswith('.safetensors'):
                #     continue

                r = {}
                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])
                r['size'] = cls.get_filesize_gigabytes(r['filepath'])

                rs.append(r)

        return rs
