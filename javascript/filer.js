
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
