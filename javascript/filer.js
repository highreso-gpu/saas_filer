const FLASK_HOST = "http://127.0.0.1:5000"
const xhrObjects = {
    checkpoints: new XMLHttpRequest(),
    loras: new XMLHttpRequest(),
    controlnet: new XMLHttpRequest(),
    vae: new XMLHttpRequest(),
    other: new XMLHttpRequest()
};

function reload_checkpoints(_, _){
    gradioApp().querySelector('#refresh_sd_model_checkpoint').click()
}

function state(button, name, title) {
    textarea = gradioApp().querySelector('#'+name+'_title textarea')
    textarea.value = title
	textarea.dispatchEvent(new Event("input", { bubbles: true }))
    gradioApp().querySelector('#state_'+name+'_button').click()
}

function load_files(button, title) {
	name = 'files'
    textarea = gradioApp().querySelector('#'+name+'_title textarea')
    textarea.value = title
	textarea.dispatchEvent(new Event("input", { bubbles: true }))
    gradioApp().querySelector('#load_'+name+'_button').click()
}

function download_files(button, title) {
	name = 'files'
    textarea = gradioApp().querySelector('#'+name+'_title textarea')
    textarea.value = title
	textarea.dispatchEvent(new Event("input", { bubbles: true }))
    gradioApp().querySelector('#download_'+name+'_button').click()
}

function rows(name){
    selected = []
    // _Select はチェックボックスのクラス名
    gradioApp().querySelectorAll('.filer_'+name+'_select').forEach(function(x){
        // チェックされているものだけ
        if(x.checked){
            // テーブル一覧 (elms[tab1][tab2]['table']) からファイル名を取得して表示
            // ex) .filer_checkpoints_backup_row
            selected.push(x.closest('.filer_'+name+'_row').dataset.title)
        }
    })

    // selected 内に書き込み（表示に関しての制御はここしかなさそう）
    gradioApp().querySelector('#filer_'+name+'_selected label textarea').value = selected.join(",");
 	return selected.join(",")
}

function select_all(name, che){
    gradioApp().querySelectorAll('.filer_'+name+'_select').forEach(function(x){
        x.checked = che
    })
	rows(name)
}

//* Flask app 経由でファイルアップロード（同名ファイルは上書き）
async function uploadFile(tab_name, target_path) {
    const endpoint = FLASK_HOST + "/upload";
    const file = document.getElementById("fileUpload_" + tab_name).files[0];
    const progressBar = document.getElementById("progressBar_" + tab_name);
    const uploadStatus = document.getElementById("uploadStatus_" + tab_name);
    const xhr = xhrObjects[tab_name];
    const formData = new FormData();

    // Initialize progress bar
    progressBar.value = 0;

    if (!file) {
        const message = "No file selected";
        console.log(message);
        uploadStatus.innerHTML = message;
        progressBar.classList.add("hidden");
        return;
    }

    if (!xhrObjects.hasOwnProperty(tab_name)) {
        console.error(`Invalid tab_name: ${tab_name}`);
        return;
    }

    // watch progress
    xhr.upload.onprogress = function(event) {
        const percentCompleted = Math.round((event.loaded * 100) / event.total);

        if (percentCompleted == 0) {
            progressBar.classList.add("hidden");
        } else {
            progressBar.classList.remove("hidden");
        }

        progressBar.value = percentCompleted;
        uploadStatus.innerHTML = "Uploading... (" + percentCompleted + "%)";
    };

    // when the upload process is completed on the frontend side
    xhr.upload.onload = function() {
        uploadStatus.innerHTML = "Saving to Target Path...";
    }

    // success
    xhr.onload = function() {
        if (xhr.status == 200) {
            const message = xhr.response;
            uploadStatus.innerHTML = message;
        } else {
            // HTTP status: 403/404/500/...
            console.log("onload status: " + xhr.status);
        }
    };

    // error (network error, cors error, etc...)
    xhr.onerror = function() {
        const message = "xhr.onerror: Network error or CORS error occurred";
        console.log(message);
        uploadStatus.innerHTML = message;
    }

    // abort (fired by cancelUpload())
    xhr.onabort = function() {
        message = "Upload was cancelled";
        console.log(message);
        uploadStatus.innerHTML = message;
        progressBar.value = 0;
        progressBar.classList.add("hidden");
    }

    // timeout (default: 0)
    xhr.ontimeout = function() {
    }

    // send request (start upload)
    progressBar.classList.remove("hidden");

    formData.append("file", file);
    formData.append("target_path", target_path);

    /**
     * イベントリスナーの後に open() を呼び出す
     * 
     * {@link https://developer.mozilla.org/ja/docs/Web/API/XMLHttpRequestUpload}
     * > // 理論的には、 open() 呼び出しの後にイベントリスナーを設定することができますが、
     * > // ブラウザーはこの部分にバグがありがち
     */
    xhr.open("POST", endpoint, true);

    xhr.send(formData);
}

function cancelUpload(tab_name) {
    const xhr = xhrObjects[tab_name];
    xhr.abort();
}
