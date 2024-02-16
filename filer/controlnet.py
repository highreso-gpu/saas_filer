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

                r = {}
                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                r['title'] = cls.get_rel_path(dir, r['filepath'])
                r['sha256_path'] = r['filepath'] + '.sha256'
                r['sha256'] = pathlib.Path(r['sha256_path']).read_text()[:10] if os.path.exists(r['sha256_path']) else ''

                rs.append(r)

        return rs

    @classmethod
    def _table(cls, tab2, rs):
        name = f"{cls.name}_{tab2}"
        code = f"""
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>Filepath</th>
                    <th>sha256</th>
                    <th>download</th>
                </tr>
            </thead>
            <tbody>
        """

        for r in rs:
            code += f"""
                <tr class="filer_{name}_row" data-title="{r['title']}">
                    <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                    <td class="filer_title">{r['title']}</td>
                    <td class="filer_sha256">{r['sha256']}</td>
                    <td><a href="/file={r['filepath']}" download>
                        <img src="https://cdn.icon-icons.com/icons2/1288/PNG/512/1499345616-file-download_85359.png" width="24" height="24">
                    </a></td>
                </tr>
                """

        code += """
            </tbody>
        </table>
        """

        return code
