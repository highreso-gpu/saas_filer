import os
from pathlib import Path
import sys
from typing import List

import gradio as gr
from modules import script_callbacks

import filer.models as filer_models
import filer.actions as filer_actions
from filer.checkpoints import FilerGroupCheckpoints
from filer.lora import FilerGroupLora
from filer.controlnet import FilerGroupControlNet
from filer.vae import FilerGroupVAE
from filer.other import FilerGroupOther

# Import from parent directory
sys.path.append(str(Path(__file__).resolve().parent.parent))
from const.load import SAAS_DOMAIN, FLASK_PORT, SUB_PATH, DATA_DIR
import scripts.common as common


elms = {}
is_default_dir_set: bool = False    #* Settings タブで Backup_Default_Dir が設定されているか
out_html = None

def js_only():
    pass

def check_backup_dir():
    global is_default_dir_set
    settings = filer_models.load_settings()
    is_default_dir_set = False
    html = ''
    if settings['backup_default_dir']:
        is_default_dir_set = True
    else:
        html = """
            <h5 style='color: red'>Settings タブからアップロード先の設定をしてください</h5>
            <h6>(Reload UI クリック後に反映されます)</h6>
        """

    return html

def save_settings(*input_settings: List[str]) -> List[str]:
    result = filer_models.save_settings(*input_settings)    # config.json 更新（なければ作成）

    #* それぞれの保存先設定を絶対パスへ変換
    # dirs = ['checkpoints', 'lora', 'controlnet', 'vae', 'other']
    dirs = ['other']
    result_list = [os.path.join(DATA_DIR, filer_models.load_backup_dir(x)) for x in dirs]

    #* 保存の成否を HTML 用に追加
    if result:
        html_message = '<h5>保存先を更新しました<h5>'   # 反映には Reload UI が必要
    else:
        html_message = '<h6 style="color: red">' \
            '保存先の更新に失敗しました<br>' \
            '※ 基準ディレクトリより上の階層には設定できません' \
            '</h6>'
    result_list.append(html_message)

    print(result_list)
    return result_list

def ui_dir(tab1):
    global elms

    if not tab1 in elms:
        elms[tab1] = {}

    with gr.Row():
        target_path = os.path.join(DATA_DIR, filer_models.load_backup_dir(tab1.lower()))
        elms[tab1]['backup_dir'] = gr.Textbox(show_label=False, info="Target Path", value=target_path, interactive=False)

def ui_set(tab1, tab2):
    """
    tab1 内で tab2（Backup）の内容を描画
    """
    global elms, out_html

    if not tab1 in elms:
        elms[tab1] = {}
    if not tab2 in elms[tab1]:
        elms[tab1][tab2] = {}

    with gr.Row():
        elms[tab1][tab2]['reload'] = gr.Button("Reload")
        elms[tab1][tab2]['select_all'] = gr.Button("Select All")
        elms[tab1][tab2]['deselect_all'] = gr.Button("Deselect All")
    with gr.Row():
        html_content = """
            <div style='margin-bottom: 0.5rem; margin-left: 0.5rem'>
                ファイル一覧を表示または更新するには Reload ボタンをクリックしてください
            </div>
        """
        gr.HTML(html_content)
    with gr.Row():
        elms[tab1][tab2]['selected'] = gr.Textbox(
            elem_id=f"filer_{tab1.lower()}_{tab2.lower()}_selected",
            label='Selected',
            lines=1,
            interactive=False
        )
    with gr.Row():
        elms[tab1][tab2]['delete'] = gr.Button("Delete")

    with gr.Row():
        #* ファイル一覧
        elms[tab1][tab2]['table'] = gr.HTML("Please push Reload button.")

    #* gradio.File Component を使わないアップロード (Component にプログレスバーが存在しないため)
    # TODO 非ホバー時にボタンの style が想定通りに適用されていない
    with gr.Row():
        global is_default_dir_set
        target_path = os.path.join(DATA_DIR, filer_models.load_backup_dir(tab1.lower()))
        html_content = f"""
            <h2>File Upload</h2>
            <div class="uploadArea">
                <div class="uploadAreaCaution">※ファイル名は全角文字に非対応です</div>
                <input type="file" class=fileInput id="fileInput_{tab1.lower()}" name="fileInput_{tab1.lower()}">
                <div>
                    <button class="btn-like-bs btn-like-bs-primary" id="uploadButton_{tab1.lower()}" onclick="uploadFile('{tab1.lower()}', '{target_path}', '{str(is_default_dir_set).lower()}')">Upload</button>
                    <button class="btn-like-bs btn-like-bs-danger" id="cancelButton_{tab1.lower()}" disabled onclick="cancelUpload('{tab1.lower()}')">Cancel</button>
                </div>
            <div>
            <div class="uploadAreaStatus">
                <progress class="hidden" id="progressBar_{tab1.lower()}" value="0" max="100"></progress>
                <div class="uploadStatus" id="uploadStatus_{tab1.lower()}"></div>
            </div>
        """
        gr.HTML(html_content)

    # TODO これを ui_set() 時にも呼びたい
    elms[tab1][tab2]['reload'].click(
        fn=getattr(globals()[f"FilerGroup{tab1}"], f"reload_{tab2.lower()}"),
        inputs=[],
        outputs=[elms[tab1][tab2]['table'], elms[tab1][tab2]['selected']],
    )

    elms[tab1][tab2]['delete'].click(
        fn=getattr(globals()[f"FilerGroup{tab1}"], f"delete_{tab2.lower()}"),
        _js="function(){return rows('"+tab1.lower()+"_"+tab2.lower()+"')}",
        inputs=[elms[tab1][tab2]['selected']],
        outputs=[elms[tab1][tab2]['table']],
    )

    elms[tab1][tab2]['select_all'].click(fn=js_only,_js="function(){return select_all('"+tab1.lower()+"_"+tab2.lower()+"', true)}")
    elms[tab1][tab2]['deselect_all'].click(fn=js_only,_js="function(){return select_all('"+tab1.lower()+"_"+tab2.lower()+"', false)}")

def on_ui_tabs():
    global out_html
    with gr.Blocks() as filer:
        with gr.Row(equal_height=True):
            out_html = gr.HTML(check_backup_dir())
        with gr.Tabs() as tabs:
            with gr.TabItem("Checkpoints"):
                ui_dir("Checkpoints")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Backup"):
                        ui_set("Checkpoints", "Backup")
            with gr.TabItem("Lora"):
                ui_dir("Lora")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Backup"):
                        ui_set("Lora", "Backup")
            with gr.TabItem("ControlNet"):
                ui_dir("ControlNet")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Backup"):
                        ui_set("ControlNet", "Backup")
            with gr.TabItem("VAE"):
                ui_dir("VAE")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Backup"):
                        ui_set("VAE", "Backup")
            with gr.TabItem("Other"):
                ui_dir("Other")
                with gr.Tabs() as tabs:
                    with gr.TabItem("Backup"):
                        ui_set("Other", "Backup")
            with gr.TabItem("Settings"):
                # with gr.Row():
                #     gr.Textbox(show_label=False, info='Base_Dir', value=DATA_DIR + os.sep, interactive=False)
                with gr.Row():
                    # html_content = """
                    #     <div style='margin-bottom: 0.5rem'>
                    #         Base_Dir 以下の各種 Backup_[Model]_Dir にファイルがアップロードされます
                    #     </div>
                    #     <ul>
                    #         <li style>Base_Dir は固定です</li>
                    #         <li>Backup_Default_Dir は設定必須です</li>
                    #         <ul>
                    #             <li>各種 Backup_[Model]_Dir に設定がない場合は Backup_Default_Dir にアップロードされます</li>
                    #         </ul>
                    #         <li>設定後はアプリケーション全体の Settings タブから Reload UI をクリックしてください</li>
                    #     </ul>
                    # """
                    html_content = """
                        <div style='margin: 0.5rem 1.0rem;'>設定後はアプリケーション全体の Settings タブから Reload UI をクリックしてください</div>
                    """
                    gr.HTML(html_content)
                settings = []
                for k, v in filer_models.load_settings().items():
                    #* Other 以外は設定非表示（変更不可）
                    if k == 'backup_other_dir':
                        with gr.Row():
                        #* labelを使ってしまうと、stable-diffusion-webui/ui-config.json にそのキーで登録され、それ以降 value 初期表示が更新できなくなるため注意
                            settings.append(gr.Textbox(show_label=False, info=k, value=v, interactive=True))
                with gr.Row():
                    apply_settings = gr.Button("Apply settings")
                with gr.Row():
                    result_message = gr.HTML("")
                with gr.Row():
                    flask_host = f"http://{SAAS_DOMAIN}:{FLASK_PORT}" if common.is_development() else f"https://{SAAS_DOMAIN}/{SUB_PATH}"
                    html_content = f"""
                        <div class="hidden" id="flaskHost">{flask_host}</div>
                    """
                    gr.HTML(html_content)

        apply_settings.click(
            fn=save_settings,
            inputs=settings,
            outputs=[
                # 各タブの Backup Dir 表示を更新
                # elms['Checkpoints']['backup_dir'],
                # elms['Lora']['backup_dir'],
                # elms['ControlNet']['backup_dir'],
                # elms['VAE']['backup_dir'],
                elms['Other']['backup_dir'],
                # save_settings の成否
                result_message,
                ])

    return (filer, "Filer", "filer"),


script_callbacks.on_ui_tabs(on_ui_tabs)
