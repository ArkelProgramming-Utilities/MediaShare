var pagenum = 0;

let grid = document.getElementById("mainGrid")

const SIZE = document.getElementsByTagName("size")[0].innerHTML;
const COLUMN_NUM = document.getElementsByTagName("columns")[0].innerHTML;

grid.style.gridTemplateColumns = "repeat(" + COLUMN_NUM +", 1fr)";

function changepage(val) {
    pagenum += val;
    document.getElementById("pagenum").innerText = pagenum;
    document.getElementById("pagenum1").innerText = pagenum;
    FetchElements("");
}

function FetchElements(dir) {
    grid.innerHTML = "";

    var myHeaders = new Headers();
    myHeaders.append("page", "0");
    myHeaders.append("dir", dir);

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
    };

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

    fetch("/media-info", requestOptions).then(response => response.json()).then(function (json) {
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
                    console.log("dir=" + dir)
                    console.log("name=" + name)
                    console.log("combo=" + dir + "\\" + name)
                    if (dir.length == 0)
                        FetchElements(name);
                    else
                        FetchElements(dir + "\\" + name);
                };


            }else{
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