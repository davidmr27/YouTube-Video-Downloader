var optionDownload = document.getElementById("optionDownload");
let url = "/list_format";
let formVideo = document.getElementById("formVideo");
let loading = document.getElementById("loading");
formVideo.onsubmit = async (e) => {
    e.preventDefault();
    download.classList.add("disabled");
    if (optionDownload.length > 1) {
        optionDownload.innerHTML = ` <option value=""> -- No hay opciones -- </option>`;
    }
    // formVideo.innerHTML = formVideo.innerHTML + `\n<div class="spinner-border" role="status" id="wait_option"></div>`;
    loading.classList.remove("visually-hidden");
    let response = await fetch(url, {
        method: 'POST',
        body: new FormData(formVideo)
    });

    loading.classList.add("visually-hidden");
    if (response.ok) {
        let result = await response.json();
        console.log(result);
        for (key in result) {
            video = result[key]
            let option = document.createElement('option');
            option.className = "select";
            option.value = video['itag'];
            option.innerHTML = `${video['res']}, ${video['size']}MB, ${video['fps']}FPS `;
            optionDownload.appendChild(option);
        }
    }
};
optionDownload.addEventListener('change', async (e) => {
    let form = document.getElementById('formVideo');
    let formdata = new FormData(form);
    data = {};
    formdata.forEach((value, key) => (data[key] = value));
    console.log(form);
    loading.classList.remove("visually-hidden");
    let response = await fetch("/video", {
        method: "POST",
        body: new FormData(form)
    });
    loading.classList.add("visually-hidden");
    let download = document.getElementById('download');
    download.classList.remove("disabled");
    let result = await response.json();
    let tempname = document.getElementById("tempname");
    tempname.value = result.tempname;
    let name_video = document.getElementById("name_video");
    name_video.value = result.name;
    
})