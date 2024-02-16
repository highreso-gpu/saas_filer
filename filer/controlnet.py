import os
import pathlib

from modules import shared, sd_models
from .base import FilerGroupBase
from . import models as filer_models
from . import actions as filer_actions

class FilerGroupControlNet(FilerGroupBase):
    name = 'contolnet'

    @classmethod
    def get_active_dir(cls):
        # TODO もし ACTIVE DIR 使うのであれば直接指定でもよいかも
        # return os.path.abspath(shared.cmd_opts.controlnet_dir)
        return "manually written path"

    @classmethod
    def _get_list(cls, dir):
        rs = []
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                # TODO 拡張子を限定する必要があるのか確認
                # if not filename.endswith('.pth') :
                #     continue

                #* filename と title 同じでは？違う場合もある？
                r = {}
                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])
                # r['sha256_path'] = r['filepath'] + '.sha256'
                # r['sha256'] = pathlib.Path(r['sha256_path']).read_text()[:10] if os.path.exists(r['sha256_path']) else ''

                rs.append(r)

        return rs
