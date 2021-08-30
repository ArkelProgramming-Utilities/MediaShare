var pagenum = 0;

const grid = document.getElementById("mainGrid")
const login_form = document.getElementById("login_form");
const login_grid = document.getElementById("login_grid");
const login_error = document.getElementById("login_error");
const login_password = document.getElementById("login_password");



function FetchElements(dir) {
    grid.innerHTML = "";
    var COLUMN_NUM = document.getElementsByTagName("columns")[0].innerHTML;
    var SIZE = document.getElementsByTagName("size")[0].innerHTML;

    grid.style.gridTemplateColumns = "repeat(" + COLUMN_NUM + ", 1fr)";


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
        redirect: 'follow'
    };

    fetch("/media-info", requestOptions).then(response => response.json()).then(function (json) {
        if (json["status_code"] == 2) {
            login_grid.style.visibility = "visible";
        }

        for (var i = 0; i < json.length; i++) {

            var elem = json[i]
            const name = elem[0]
            const type = elem[1]
            const index_ = i;

            var grid_item = document.createElement("div");
            grid_item.classList = "grid-item";



            var media = null;
            if (type == "img") {
                media = document.createElement("img");
                media.id = "elem_" + index_;

                grid_item.onclick = function () {
                    var myHeaders = new Headers();
                    myHeaders.append("file", name);
                    myHeaders.append("size", "-1");

                    var requestOptions = {
                        method: 'GET',
                        headers: myHeaders,
                        credentials: "same-origin",
                        redirect: 'follow'
                    };

                    fetch("get-media", requestOptions)
                        .then(response => response.blob())
                        .then(function (data) {
                            let node = document.getElementById("elem_" + index_)
                            node.src = URL.createObjectURL(data);
                        });
                };

                var myHeaders = new Headers();
                myHeaders.append("file", name);
                myHeaders.append("size", SIZE);

                var requestOptions = {
                    method: 'GET',
                    headers: myHeaders,
                    credentials: "same-origin",
                    redirect: 'follow'
                };

                fetch("get-media", requestOptions)
                    .then(response => response.blob())
                    .then(function (data) {
                        let node = document.getElementById("elem_" + index_)
                        node.src = URL.createObjectURL(data);
                    });
            } else if (type == "vid") {
                media = document.createElement("video");
                media.id = "elem_" + index_;

                var myHeaders = new Headers();
                myHeaders.append("file", name);

                var requestOptions = {
                    method: 'GET',
                    headers: myHeaders,
                    credentials: "same-origin",
                    redirect: 'follow'
                };

                fetch("get-media", requestOptions)
                    .then(response => response.blob())
                    .then(function (data) {
                        let node = document.getElementById("elem_" + index_)
                        node.src = URL.createObjectURL(data);
                    });
                media.setAttribute('controls', '');
            } else if (type == "txt") {
                media = document.createElement("p");
                media.id = "elem_" + index_;

                var myHeaders = new Headers();
                myHeaders.append("file", name);
                myHeaders.append("size", "36");

                var requestOptions = {
                    method: 'GET',
                    headers: myHeaders,
                    credentials: "same-origin",
                    redirect: 'follow'
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
                    if (dir.length == 0)
                        FetchElements(name);
                    else
                        FetchElements(dir + "\\" + name);
                };


            } else {
                media = document.createElement("div")
            }

            media.classList = "media-item";


            var title = document.createElement("h3");
            title.classList = "title-media-item";
            title.innerText = name;


            grid_item.appendChild(media);
            grid_item.appendChild(title);
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
                FetchElements("");
            } else if (code == 1) {
                login_error.innerText = "invalid password";
                login_password.value = "";
            }
        });
});