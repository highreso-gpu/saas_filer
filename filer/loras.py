import os
import pathlib

from modules import sd_models, shared
from .base import FilerGroupBase
from . import models as filer_models
from . import actions as filer_actions

class FilerGroupLoras(FilerGroupBase):
    name = 'loras'

    @classmethod
    def get_active_dir(cls):
        return os.path.abspath(shared.cmd_opts.lora_dir)

    @classmethod
    def _get_list(cls, dir):
        rs = []
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                # if not filename.endswith('.pt') and not filename.endswith('.safetensors'):
                #     continue

                r = {}
                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])
                r['sha256_path'] = r['filepath'] + '.sha256'
                r['sha256'] = pathlib.Path(r['sha256_path']).read_text()[:10] if os.path.exists(r['sha256_path']) else ''

                rs.append(r)

        return rs
