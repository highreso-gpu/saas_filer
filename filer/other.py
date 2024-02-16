import os
import pathlib

from modules import shared, sd_models
from .base import FilerGroupBase
from . import models as filer_models
from . import actions as filer_actions

class FilerGroupOther(FilerGroupBase):
    name = 'other'

    @classmethod
    def get_active_dir(cls):
        # TODO もし ACTIVE DIR 使うのであれば直接指定でもよいかも
        # return os.path.abspath(shared.cmd_opts.other_dir)
        return "manually written path"

    @classmethod
    def _get_list(cls, dir):
        rs = []
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                r = {}
                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])

                rs.append(r)

        return rs
