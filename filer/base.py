import os
import pathlib
import yaml
import torch
from safetensors.torch import save_file

from modules import sd_models
from . import models as filer_models
from . import actions as filer_actions

class FilerGroupBase:
    name = ''
    upload_zip = False

    @classmethod
    # 子クラスでそれぞれ定義
    def get_active_dir(cls):
        return ''

    @classmethod
    def get_backup_dir(cls):
        return filer_models.load_backup_dir(cls.name)

    @classmethod
    def get_dir(cls, tab2):
        if tab2 == 'active':
            return cls.get_active_dir()
        elif tab2 == 'backup':
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
    def list_active(cls):
        return cls._get_list(cls.get_active_dir())

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
    def download_urls(cls, urls):
        filer_actions.urls(urls, cls.get_active_dir())
        return 'Downloaded.'

    @classmethod
    def copy_active(cls, filenames):
        filer_actions.copy(filenames, cls.list_active(), cls.get_backup_dir())
        return cls.table_active()

    @classmethod
    def copy_backup(cls, filenames):
        filer_actions.copy(filenames, cls.list_backup(), cls.get_active_dir())
        return cls.table_backup()

    @classmethod
    def move_active(cls, filenames):
        filer_actions.move(filenames, cls.list_active(), cls.get_backup_dir())
        return cls.table_active()

    @classmethod
    def move_backup(cls, filenames):
        filer_actions.move(filenames, cls.list_backup(), cls.get_active_dir())
        return cls.table_backup()

    @classmethod
    def delete_active(cls, filenames):
        filer_actions.delete(filenames, cls.list_active())
        return cls.table_active()

    @classmethod
    def delete_backup(cls, filenames):
        filer_actions.delete(filenames, cls.list_backup())
        return cls.table_backup()

    @classmethod
    def calc_active(cls, filenames):
        filer_actions.calc_sha256(filenames, cls.list_active())
        return cls.table_active()

    @classmethod
    def calc_backup(cls, filenames):
        filer_actions.calc_sha256(filenames, cls.list_backup())
        return cls.table_backup()

    @classmethod
    def save_comment(cls, data):
        filer_models.save_comment(cls.name, data)
        return 'saved.'

    @classmethod
    def download_active(cls, filenames):
        return filer_actions.download(filenames, cls.list_active())

    @classmethod
    def download_backup(cls, filenames):
        return filer_actions.download(filenames, cls.list_backup())

    @classmethod
    def upload_active(cls, files):
        return filer_actions.upload(files, cls.get_active_dir(), cls.upload_zip)

    @classmethod
    def upload_backup(cls, files):
        #* return 中身なし
        return filer_actions.upload(files, cls.get_backup_dir(), cls.upload_zip)

    @classmethod
    def table_active(cls):
        return cls._table("active", cls.list_active())

    @classmethod
    def table_backup(cls):
        return cls._table("backup", cls.list_backup())

    @classmethod
    def reload_active(cls):
        return [cls.table_active(), '']

    @classmethod
    def reload_backup(cls):
        return [cls.table_backup(), '']

    @classmethod
    def get_filesize_kilobytes(cls, filepath: str) -> str:
        """
        ファイルサイズをカンマありの KB 単位で取得
        小数点第2位まで表示（第3位を四捨五入）
        """
        filesize = os.path.getsize(filepath)
        kilobytes = round(filesize / 1024, 2)

        return "{:,.2f}".format(kilobytes)

    # @classmethod
    # def _table(cls, name, rs):
    #     pass

    @classmethod
    def _table(cls, tab2, rs):
        name = f"{cls.name}_{tab2}"

        # TODO ここにディレクトリの使用容量を追加で表示したい
        code = f"""
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>file</th>
                    <th>size[KB]</th>
                    <th>download</th>
                </tr>
            </thead>
            <tbody>
        """

        for r in rs:
            code += f"""
                <tr class="filer_{name}_row" data-title="{r['title']}">
                    <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows('{name}')"></td>
                    <td class="filer_title">{r['title']}</td>
                    <td style="text-align: right">{r['size']}</td>
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
