import os
import pathlib
import html
import yaml
import torch
import pprint

from modules import sd_models
from modules.shared import opts, cmd_opts, state
from modules.controlnet import controlnet

from .base import FilerGroupBase
from . import models as filer_models
from . import actions as filer_actions

class FilerGroupControlNet(FilerGroupBase):
    # 必要？外部で参照している？
    name = 'controlnet'

    @classmethod
    def get_active_dir(cls):
        return os.path.abspath(cmd_opts.controlnet_dir)
        # return "hogehoge"
        #* cmd_opts を辿る
        """
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/shared.py
        from modules import shared_cmd_options, shared_gradio_themes, options, shared_items, sd_models_types
        cmd_opts = shared_cmd_options.cmd_opts
        """
        #* 下 （shared_cmd_options を辿る）
        """
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/shared_cmd_options.py
        parser = cmd_args.parser

        if os.environ.get('IGNORE_CMD_ARGS_ERRORS', None) is None:
            cmd_opts = parser.parse_args()
        else:
            cmd_opts, _ = parser.parse_known_args()
        """
        #* 下 （cmd_args を辿る）
        """
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/cmd_args.py
        import argparse  #  python 標準の parser
        parser = argparse.ArgumentParser()
        parser.add_argument("--hypernetwork-dir", type=str, default=os.path.join(models_path, 'hypernetworks'), help="hypernetwork directory"
        """
        #*** 結論； 1111 に記述がないとダメ？？

    @classmethod
    def state(cls, tab2, filename):

        filepath = os.path.join(cls.get_dir(tab2), filename)

        if not os.path.exists(filepath):
            raise ValueError(f"Not found {filepath}")

        r = {}
        state_dict = torch.load(filepath, map_location='cpu')
        r['name'] = state_dict.get('name', None)
        r['layer_structure'] = state_dict.get('layer_structure', [1, 2, 1])
        r['activation_func'] = state_dict.get('activation_func', None)
        r['weight_init'] = state_dict.get('weight_initialization', 'Normal')
        r['add_layer_norm'] = state_dict.get('is_layer_norm', False)
        r['use_dropout'] = state_dict.get('use_dropout', False)
        r['activate_output'] = state_dict.get('activate_output', True)
        r['last_layer_dropout'] = state_dict.get('last_layer_dropout', False)
        optimizer_saved_dict = torch.load(filepath + '.optim', map_location = 'cpu') if os.path.exists(filepath + '.optim') else {}
        r['optimizer_name'] = optimizer_saved_dict.get('optimizer_name', 'AdamW')
        r['optimizer_hash'] = optimizer_saved_dict.get('hash', None)
        r['optimizer_state_dict'] = optimizer_saved_dict.get('optimizer_state_dict', None)

        return r

    @classmethod
    def state_active(cls, title):
        html = title + '<br><pre>' + pprint.pformat(cls.state('active', title)) + '</pre>'
        return html

    @classmethod
    def state_backup(cls, title):
        html = title + '<br><pre>' + pprint.pformat(cls.state('backup', title)) + '</pre>'
        return html

    @classmethod
    def _get_list(cls, dir):
        rs = []
        for filedir, subdirs, filenames in os.walk(dir):
            for filename in filenames:
                if not filename.endswith('.pt'):
                    continue

                r = {}

                r['filename'] = filename
                r['filepath'] = os.path.join(filedir, filename)
                # r['prompt'] = html.escape(f"<hypernet:{pathlib.Path(r['filepath']).stem}:1.0>")
                #* 元の構造が hypernetwork でないため違いそう
                r['prompt'] = html.escape(f"<controlnet:{pathlib.Path(r['filepath']).stem}:1.0>")
                r['title'] = cls.get_rel_path(dir, r['filepath'])
                r['hash'] = sd_models.model_hash(r['filepath'])
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
                    <th>Prompt</th>
                    <th>state</th>
                    <th>hash</th>
                    <th>sha256</th>
                </tr>
            </thead>
            <tbody>
        """

        for r in rs:
            code += f"""
                <tr class="filer_{name}_row" data-title="{r['title']}">
                    <td class="filer_checkbox"><input class="filer_{name}_select" type="checkbox" onClick="rows_{name}()"></td>
                    <td class="filer_title">{r['title']}</td>
                    <td class="filer_prompt">{r['prompt']}</td>
                    <td class="filer_state"><input onclick="state(this, '{name}', '{r['title']}')" type="button" value="state" class="gr-button gr-button-lg gr-button-secondary"></td>
                    <td class="filer_hash">{r['hash']}</td>
                    <td class="filer_sha256">{r['sha256']}</td>
                </tr>
                """

        code += """
            </tbody>
        </table>
        """

        return code
