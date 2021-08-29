var pagenum = 0;

  let grid = document.getElementById("mainGrid")

  function changepage(val) {
    pagenum += val;
    document.getElementById("pagenum").innerText = pagenum;
    document.getElementById("pagenum1").innerText = pagenum;
    FetchElements();
  }

  function FetchElements() {
    console.log("Console works")
    grid.innerHTML = "";
    fetch("/media-info/" + pagenum).then(function (response) {
      response.json().then(function (json) {
        for (var i = 0;i<json.length;i++) {

          var elem = json[i]
          let elemid = elem[0];

          var grid_item = document.createElement("div");
          grid_item.classList = "grid-item";

        
          var media = null;
          
          if (elem[2] == "img") {
            media = document.createElement("img");
            media.src = "get-media/" + elemid + "?size=256";
            
            grid_item.onclick = function(){
              let elem1 = document.getElementById("elem_" + elemid)
              elem1.src = "get-media/" + elemid;
            };
          } else if (elem[2] == "vid") {
            media = document.createElement("video");
            media.setAttribute('controls', '');
            
            var src = document.createElement("source");
            src.src = "get-media/" + elemid;
            src.type = "video/" + elem[3];
            media.appendChild(src);
          } else {
            media = document.createElement("p");
            const contentsize = 256;

            fetch("/get-media/" + elemid, {
            }).then(function (response) {
                response.text().then(function (txt) {
                  if (txt.length > contentsize)
                    media.innerText = txt.substr(0, contentsize);
                  else
                    media.innerText = txt;
                });
              });

          }
          media.classList = "media-item";
          media.id = "elem_" + elemid;

          var title = document.createElement("h3");
          title.classList = "title-media-item";
          title.innerText = elem[1];



          grid_item.appendChild(media);
          grid_item.appendChild(title);
          grid.appendChild(grid_item);
        }
      });
    });
  }

  FetchElements();