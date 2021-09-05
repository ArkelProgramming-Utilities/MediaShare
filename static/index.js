var pagenum = 0;

const grid = document.getElementById("mainGrid")
const login_form = document.getElementById("login_form");
const login_grid = document.getElementById("login_grid");
const login_error = document.getElementById("login_error");
const login_password = document.getElementById("login_password");
const media_preview = document.getElementById("media_preview");
const image_preview = document.getElementById("image_preview");
const video_preview = document.getElementById("video_preview");
const text_preview = document.getElementById("text_preview");
const image_preview_p = document.getElementById("image_preview_p");
const video_preview_p = document.getElementById("video_preview_p");
const text_preview_p = document.getElementById("text_preview_p");

function hidePreview() {
    media_preview.style.visibility = "collapse";
    video_preview_p.style.visibility = "collapse";
    image_preview_p.style.visibility = "collapse";
    text_preview_p.style.visibility = "collapse";
    image_preview.src = "";
    video_preview.src = "";
    text_preview.innerText = ""
}

function FetchElements(dir) {
    grid.innerHTML = "";
    var controller = new AbortController();
    var { signal } = controller;

    if (dir.length > 0) {
        var grid_item = document.createElement("div");
        grid_item.classList = "grid-item";

        media = document.createElement("img")
        media.id = "back_folder";
        media.classList = "media-item";
        media.src = "static/folder.png";

        grid_item.onclick = function () {
            dirs = dir.split("\\")
            dirs.pop()
            controller.abort()
            FetchElements(dirs.join("\\"));
        };


        var title = document.createElement("h3");
        title.classList = "title-media-item";
        title.innerText = "parent";


        grid_item.appendChild(media);
        grid_item.appendChild(title);
        grid.appendChild(grid_item);
    }

    var myHeaders = new Headers();
    myHeaders.append("page", "0");
    myHeaders.append("dir", dir);

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        credentials: "same-origin",
        redirect: 'follow',
        signal
    };

    fetch("/media-info", requestOptions).then(response => response.json()).then(function (json) {
        if (json["status_code"] == 2) {
            login_grid.style.visibility = "visible";
            grid.style.visibility = "collapse";
        }

        for (var i = 0; i < json.length; i++) {

            var elem = json[i]
            const name = elem[0]
            const type = elem[1]
            console.log(elem.length)
            if (elem.length >2){
                var raw_timestamp = parseInt(elem[2])
            }else{
                var raw_timestamp = 0;
            }
            const index_ = i;


            const dateObject = new Date(raw_timestamp * 1000);
            const humanDateFormat = dateObject.toLocaleString();

            var grid_item = document.createElement("div");
            grid_item.classList = "grid-item";



            var media = null;
            if (type == "img" || type == "imgc") {
                media = document.createElement("img");
                media.id = "elem_" + index_;

                grid_item.onclick = function () {
                    var myHeaders = new Headers();
                    myHeaders.append("file", name);

                    var requestOptions = {
                        method: 'GET',
                        headers: myHeaders,
                        credentials: "same-origin",
                        redirect: 'follow',
                        signal
                    };
                    media_preview.style.visibility = "visible";
                    fetch("get-media", requestOptions)
                        .then(response => response.blob())
                        .then(function (data) {

                            image_preview_p.style.visibility = "visible";
                            image_preview.src = URL.createObjectURL(data);
                        });
                };

                var myHeaders = new Headers();
                myHeaders.append("file", name);
                myHeaders.append("mod", "p");

                var requestOptions = {
                    method: 'GET',
                    headers: myHeaders,
                    credentials: "same-origin",
                    redirect: 'follow',
                    signal
                };

                fetch("get-media", requestOptions)
                    .then(response => response.blob())
                    .then(function (data) {
                        let node = document.getElementById("elem_" + index_)
                        node.src = URL.createObjectURL(data);
                    });
            } else if (type == "vid" || type == "vidc") {
                media = document.createElement("img");
                media.id = "elem_" + index_;

                grid_item.onclick = function () {
                    var myHeaders = new Headers();
                    myHeaders.append("file", name);

                    var requestOptions = {
                        method: 'GET',
                        headers: myHeaders,
                        credentials: "same-origin",
                        redirect: 'follow',
                        signal
                    };

                    media_preview.style.visibility = "visible";

                    fetch("get-media", requestOptions)
                        .then(response => response.blob())
                        .then(function (data) {
                            video_preview_p.style.visibility = "visible";
                            video_preview.src = URL.createObjectURL(data);
                        });
                };

                var myHeaders = new Headers();
                myHeaders.append("file", name);
                myHeaders.append("mod", "t");

                var requestOptions = {
                    method: 'GET',
                    headers: myHeaders,
                    credentials: "same-origin",
                    redirect: 'follow',
                    signal
                };

                fetch("get-media", requestOptions)
                    .then(response => response.blob())
                    .then(function (data) {
                        let node = document.getElementById("elem_" + index_)
                        node.src = URL.createObjectURL(data);
                    });
            } else if (type == "txt") {
                media = document.createElement("p");
                media.id = "elem_" + index_;

                grid_item.onclick = function () {
                    var myHeaders = new Headers();
                    myHeaders.append("file", name);

                    var requestOptions = {
                        method: 'GET',
                        headers: myHeaders,
                        credentials: "same-origin",
                        redirect: 'follow',
                        signal
                    };

                    media_preview.style.visibility = "visible";

                    fetch("get-media", requestOptions)
                        .then(response => response.text())
                        .then(function (data) {
                            text_preview_p.style.visibility = "visible";
                            text_preview.innerText = data;
                        });
                };


                var myHeaders = new Headers();
                myHeaders.append("file", name);
                myHeaders.append("mod", "p");

                var requestOptions = {
                    method: 'GET',
                    headers: myHeaders,
                    credentials: "same-origin",
                    redirect: 'follow',
                    signal
                };

                fetch("get-media", requestOptions)
                    .then(response => response.text())
                    .then(function (data) {
                        let node = document.getElementById("elem_" + index_)
                        node.innerText = data;
                    });


            } else if (type == "dir") {
                media = document.createElement("img")
                media.id = "elem_" + index_;
                media.src = "static/folder.png";

                grid_item.onclick = function () {
                    controller.abort()
                    if (dir.length == 0) {
                        FetchElements(name);
                    }
                    else {
                        FetchElements(dir + "\\" + name);
                    }
                };


            } else {
                media = document.createElement("div")
            }

            media.classList = "media-item";
            grid_item.appendChild(media);

            var title = document.createElement("h3");
            title.classList = "title-media-item";
            title.innerText = name.split("\\")[name.split("\\").length - 1]
            grid_item.appendChild(title);

            if(raw_timestamp!=0){
                var date = document.createElement("h3");
                date.classList = "title-media-item";

                date.innerText = humanDateFormat;
                grid_item.appendChild(date);
                }



            grid.appendChild(grid_item);
        }
    });
}

FetchElements("");

login_form.addEventListener("submit", function (event) {
    event.preventDefault();

    var formData = new FormData(login_form);

    var requestOptions = {
        method: "POST",
        body: formData,
        redirect: 'follow'
    };
    fetch("/auth", requestOptions)
        .then(response => response.json())
        .then(function (data) {
            code = data["status_code"]
            if (code == 0) {
                var token = data["auth_token"];
                document.cookie = "auth_token=" + token + ";Secure";
                login_grid.style.visibility = "collapse";
                grid.style.visibility = "visible";
                FetchElements("");
            } else if (code == 1) {
                login_error.innerText = "invalid password";
                login_password.value = "";
            }
        });
});