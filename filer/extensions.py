import os
import pathlib
import yaml
import torch

from modules import sd_models
from modules.shared import opts, cmd_opts, state
from modules.extensions import extensions_dir

from .base import FilerGroupBase
from . import models as filer_models

class FilerGroupExtensions(FilerGroupBase):
    name = 'extensions'
    upload_zip = True

    @classmethod
    def get_active_dir(cls):
        return extensions_dir

    @classmethod
    def _get_list(cls, dir):
        p = pathlib.Path(__file__).parts[-3]

        rs = []
        for filename in os.listdir(dir):
            # 自分自身は対象外
            if filename == p:
                continue
            # ファイルは対象外
            if not os.path.isdir(os.path.join(dir, filename)):
                continue

            r = {}
            r['title'] = filename
            r['filename'] = filename
            r['filepath'] = os.path.join(dir, filename)

            rs.append(r)

        return rs
