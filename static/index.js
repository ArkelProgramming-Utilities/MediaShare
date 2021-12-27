var pagenum = 0;

let grid = document.getElementById("mainGrid")
let login_form = document.getElementById("login_form");
let login_grid = document.getElementById("login_grid");
let login_error = document.getElementById("login_error");
let login_password = document.getElementById("login_password");
let media_preview = document.getElementById("media_preview");
let image_preview = document.getElementById("image_preview");
let video_preview = document.getElementById("video_preview");
let text_preview = document.getElementById("text_preview");
let image_preview_p = document.getElementById("image_preview_p");
let video_preview_p = document.getElementById("video_preview_p");
let text_preview_p = document.getElementById("text_preview_p");
let navleft = document.getElementById("navleft");
let navright = document.getElementById("navright");

function hidePreview() {
    media_preview.style.visibility = "collapse";
    video_preview_p.style.visibility = "collapse";
    image_preview_p.style.visibility = "collapse";
    text_preview_p.style.visibility = "collapse";
    image_preview.src = "";
    video_preview.src = "";
    text_preview.innerText = ""
}

var controller2 = null;

function showPreview(index) {
    if(index<0||index>=media_data.length)
        return false;

    if(controller2!=null)
        controller2.abort();
    controller2 = new AbortController();
    var { signal2 } = controller2;

    file = media_data[index][0];
    type = media_data[index][1];

    hidePreview();
    var myHeaders = new Headers();
    myHeaders.append("file", file);
    
    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        credentials: "same-origin",
        redirect: 'follow',
        signal2
    };
    media_preview.style.visibility = "visible";
    if (type == "img" || type == "imgc") {
        fetch("get-media", requestOptions)
            .then(response => response.blob())
            .then(function (data) {

                image_preview_p.style.visibility = "visible";
                image_preview.src = URL.createObjectURL(data);
            });
    } else if (type == "vid" || type == "vidc") {
        fetch("get-media", requestOptions)
            .then(response => response.blob())
            .then(function (data) {
                video_preview_p.style.visibility = "visible";
                video_preview.src = URL.createObjectURL(data);
            });
    } else if (type == "txt") {
        fetch("get-media", requestOptions)
            .then(response => response.text())
            .then(function (data) {
                text_preview_p.style.visibility = "visible";
                text_preview.innerText = data;
            });
    }
    return true;
}


var media_index = -1;
var media_data = [];
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

        media_data = [];
        for(var i = 0;i<json.length;i++){
            media_data.push(json[i]);
        }

        for (var i = 0; i < json.length; i++) {

            var elem = media_data[i]

            const file = elem[0]
            const type = elem[1]
            var name_ = 0;
            if (elem.length > 2) {
                name_ = elem[2]
                var raw_timestamp = parseInt(elem[3])
            } else {
                var raw_timestamp = -1;
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
                    media_index = index_;
                    
                    showPreview(index_);
                };

                var myHeaders = new Headers();
                myHeaders.append("file", file);
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
                    media_index = index_;
                    
                    showPreview(index_);
                };

                var myHeaders = new Headers();
                myHeaders.append("file", file);
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
                    media_index = index_;
                    
                    showPreview(index_);
                };


                var myHeaders = new Headers();
                myHeaders.append("file", file);
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
                        FetchElements(file);
                    }
                    else {
                        FetchElements(dir + "\\" + file);
                    }
                };


            } else {
                media = document.createElement("div")
            }

            media.classList = "media-item";
            grid_item.appendChild(media);

            var title = document.createElement("h3");
            title.classList = "title-media-item";
            if (name_ == 0)
                title.innerText = file.split("\\")[file.split("\\").length - 1];
            else
                title.innerText = name_;
            grid_item.appendChild(title);

            if (name_ != 0) {
                var title2 = document.createElement("h6");
                title2.classList = "title-media-item";

                title2.innerText = file.split("\\")[file.split("\\").length - 1];
                title2.style.color = "RED";
                grid_item.appendChild(title2);
            }

            if (raw_timestamp != -1) {
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

media_preview.addEventListener('click', function (e) {
    hidePreview();
});

image_preview.addEventListener('click', function (e) {
    e.stopPropagation();
    console.log("clicked image");
});
text_preview.addEventListener('click', function (e) {
    e.stopPropagation();
    console.log("clicked text");
});
video_preview.addEventListener('click', function (e) {
    e.stopPropagation();
    console.log("clicked video");
});

navleft.addEventListener('click', function (e) {
    e.stopPropagation();
    media_index--;
    var ret = showPreview(media_index);
    if(ret==false)
        media_index++;
    console.log("clicked left");
});

navright.addEventListener('click', function (e) {
    e.stopPropagation();
    media_index++;
    var ret = showPreview(media_index);
    if(ret==false)
        media_index--;
    console.log("clicked right");
});
