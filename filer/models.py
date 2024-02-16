import os
import pathlib
import json

# https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/sd_models.py
from modules import sd_models

"""
Backup Dir の読込と更新
設定パス: stable-diffusion-webui/extensions/saas_filer/config/config.json
"""

default_settings = {
    'backup_default_dir': '',
    'backup_checkpoints_dir': '',
    # 'backup_embeddings_dir': '',
    # 'backup_dreambooths_dir': '',
    'backup_loras_dir': '',
    # 'backup_hypernetworks_dir': '',
    'backup_controlnet_dir': '',
    'backup_vae_dir': '',
    'backup_other_dir': '',
    # 'backup_extensions_dir': '',
    # 'backup_images_dir': '',
    }

#* 全体の設定を取得
def load_settings():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'config.json')
    # print("filepath: {}".format(filepath))
    settings = default_settings
    if os.path.exists(filepath):
        with open(filepath) as f:
            settings.update(json.load(f))
    return settings

#* それぞれ有効な Backup Dir のパスを取得
def load_backup_dir(name):
    settings = load_settings()

    dir = ''
    # タブ毎の固有の設定（key があってそれが有効である場合）
    if 'backup_'+name+'_dir' in settings and settings['backup_'+name+'_dir']:
        dir = settings['backup_'+name+'_dir']
    # タブ毎の固有の設定がない場合は backup_default_dir を使う
    elif 'backup_default_dir' in settings and settings['backup_default_dir']:
        dir = os.path.join(settings['backup_default_dir'], name)

    # config.json に設定があるがパスが存在しない場合は再起的にディレトリを作成
    if dir and not os.path.exists(dir):
        os.makedirs(dir)

    # 設定がなければ何もしない

    return dir

def save_settings(*input_settings):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'config.json')
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    i = 0
    for k in default_settings.keys():
        data.update({k: input_settings[i]})
        i += 1
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, "w") as f:
        json.dump(data, f)
    # return json.dumps(data)
    return
