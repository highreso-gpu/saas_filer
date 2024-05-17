import os
import traceback


class FileSize:
    UNITS = {"B": 0, "KB": 1, "MB": 2, "GB": 3, "TB": 4}

    @classmethod
    def convert(cls, filesize: int, unit: str) -> str:
        """
        ファイルサイズを指定した単位に変換
        小数点第3位まで表示（第4位を四捨五入）
        """
        if unit not in cls.UNITS:
            raise ValueError("Invalid unit. Choose from 'B', 'KB', 'MB', 'GB', 'TB'.")

        converted = round(filesize / 1024 ** cls.UNITS[unit], 3)
        return "{:,.3f}".format(converted)

    @classmethod
    def get_filesize(cls, filepath: str, unit: str) -> str:
        """パスからファイルサイズを指定単位で取得"""
        filesize = os.path.getsize(filepath)
        return cls.convert(filesize, unit)

    @classmethod
    def get_dir_size(cls, path: str, unit: str) -> int:
        """path 以下のディレクトリの使用容量を再帰的に集計して指定単位で取得"""
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

        # return total_size
        return cls.convert(total_size, unit)
