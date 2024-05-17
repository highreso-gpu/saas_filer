import os
from pathlib import Path
import sys
from urllib.parse import urljoin

from . import actions as filer_actions
from . import models as filer_models
from .util import FileSize

# Import from parent directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from const.load import SAAS_DOMAIN, SUB_PATH
import scripts.common as common


class FilerGroupBase:
    name = ''
    upload_zip = False

    @classmethod
    def get_backup_dir(cls):
        return filer_models.load_backup_dir(cls.name)

    @classmethod
    def get_dir(cls, tab2):
        if tab2 == 'backup':
            return cls.get_backup_dir()
        return ''

    @classmethod
    def get_rel_path(cls, dir, path):
        return path.replace(dir, '').replace(os.sep, '/').lstrip('/')

    @classmethod
    # 子クラスでそれぞれ定義
    def _get_list(cls, dir):
        pass

    @classmethod
    def list_backup(cls):
        backup_dir = cls.get_backup_dir()
        if not backup_dir or not os.path.exists(backup_dir):
            return []
        # print("[list_backup] ---------------------------------------")
        # print(cls._get_list(backup_dir))
        # print("-----------------------------------------------------")
        return cls._get_list(backup_dir)

    @classmethod
    def delete_backup(cls, filenames):
        filer_actions.delete(filenames, cls.list_backup())
        return cls.table_backup()

    @classmethod
    def table_backup(cls):
        return cls._table("backup", cls.list_backup())

    @classmethod
    def reload_backup(cls):
        return [cls.table_backup(), '']

    # @classmethod
    # def _table(cls, name, rs):
    #     pass

    @classmethod
    def _table(cls, tab2, rs):
        name = f"{cls.name}_{tab2}"
        dir_path = cls.get_dir(tab2)
        unit = 'GB'
        dir_size_unit = FileSize().get_dir_size(dir_path, unit)

        code = f"""
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>file</th>
                    <th>size[{unit}]</th>
                    <th>download</th>
                </tr>
            </thead>
            <tbody>
        """

        gradio_port = 7860
        base_url = f"http://{SAAS_DOMAIN}:{gradio_port}" if common.is_development() else f"https://{SAAS_DOMAIN}/{SUB_PATH}"

        for r in rs:
            file_path = f"file={r['filepath']}"
            download_link = urljoin(base_url, file_path)
            code += f"""
                <tr class="filer_{name}_row" data-title="{r['title']}">
                    <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows('{name}')"></td>
                    <td class="filer_title">{r['title']}</td>
                    <td style="text-align: right">{r['size']}</td>
                    <td><a href="{download_link}" download>
                        <img src="https://cdn.icon-icons.com/icons2/1288/PNG/512/1499345616-file-download_85359.png" width="24" height="24">
                    </a></td>
                </tr>
                """

        code += f"""
            </tbody>
        </table>
        <div class="dir_usage">Total Disk Usage of Target Path: {dir_size_unit} {unit}</div>
        """

        return code
