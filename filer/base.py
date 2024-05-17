import os
from pathlib import Path
import sys
import traceback
from urllib.parse import urljoin

from . import actions as filer_actions
from . import models as filer_models

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
    # def convert_to_kilobytes(cls, filesize: int) -> str:
    #     """
    #     ファイルサイズをカンマありの KB 単位へ
    #     変換
    #     小数点第2位まで表示（第3位を四捨五入）
    #     """
    #     kilobytes = round(filesize / 1024, 2)
    #     return "{:,.2f}".format(kilobytes)

    # @classmethod
    # def get_filesize_kilobytes(cls, filepath: str) -> str:
    #     """パスからファイルサイズを KB 単位で取得"""
    #     filesize = os.path.getsize(filepath)
    #     return cls.convert_to_kilobytes(filesize)

    @classmethod
    def convert_to_gigabytes(cls, filesize: int) -> str:
        """
        ファイルサイズをカンマありの GB 単位へ
        変換
        小数点第3位まで表示（第4位を四捨五入）
        """
        gigabytes = round(filesize / 1024 ** 3, 3)
        return "{:,.3f}".format(gigabytes)

    @classmethod
    def get_filesize_gigabytes(cls, filepath: str) -> str:
        """パスからファイルサイズを GB 単位で取得"""
        filesize = os.path.getsize(filepath)
        return cls.convert_to_gigabytes(filesize)

    @classmethod
    def get_directory_size(cls, path: str) -> int:
        """path 以下のディレクトリの使用容量を再帰的に集計して取得"""
        total_size = 0
        try:
            # 【確認用】手動で OSError を発生
            # os.path.getsize("test/path/noexist.txt")

            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
        except OSError as e:
            print("-------------------------------------------------------------------------------------------------------------------")
            print(f"An error occurred in function {traceback.extract_tb(e.__traceback__)[0][2]}: {e}")
            print("-------------------------------------------------------------------------------------------------------------------")

        return total_size

    # @classmethod
    # def _table(cls, name, rs):
    #     pass

    @classmethod
    def _table(cls, tab2, rs):
        name = f"{cls.name}_{tab2}"
        # directoryのサイズを取得
        dir_path = cls.get_dir(tab2)
        dir_size = cls.get_directory_size(dir_path)
        dir_size_g = cls.convert_to_gigabytes(dir_size)

        code = f"""
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>file</th>
                    <th>size[GB]</th>
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
        <div class="dir_usage">Total Disk Usage of Target Path: {dir_size_g} GB</div>
        """

        return code
