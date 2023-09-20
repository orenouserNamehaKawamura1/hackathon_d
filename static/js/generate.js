var dropArea = document.getElementById('drop-area')

dropArea.addEventListener('dragenter', function (e) {
  e.preventDefault()
  // クラス名を追加
  dropArea.classList.add('active')
  console.log('dragenter')
})

dropArea.addEventListener('dragleave', function (event) {
  insideDragArea = false
  console.log('dragleave')
  if ([...event.target.classList].includes('item')) {
    return
  }
  dropArea.classList.remove('active')
})

dropArea.addEventListener('drop', function (e) {
  e.preventDefault()
  dropArea.classList.remove('active')

  var file = e.dataTransfer.files[0]
  var formData = new FormData()
  formData.append('file', file)

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message)
    })
})

var DnDUploader = function (base_id) {
  if(typeof(base_id) != "string" || base_id.length == 0 || document.getElementById(base_id) == null)
    return false;

  var __body = document.getElementsByTagName('body')[0];
  var parent = document.getElementById(base_id);
  __body.addEventListener("drop", function(e){e.stopPropagation();e.preventDefault();}, false);
  __body.addEventListener("dragenter", function(e){e.stopPropagation();e.preventDefault();}, false);
  __body.addEventListener("dragover", function(e){e.stopPropagation();e.preventDefault();}, false);
  parent.addEventListener("drop", function(e){e.stopPropagation();e.preventDefault();_handleDrop(e);}, false);
  parent.addEventListener("dragenter", function(e){e.stopPropagation();e.preventDefault();}, false);
  parent.addEventListener("dragover", function(e){e.stopPropagation();e.preventDefault();}, false);

  var _handleDrop = function(e) {
    var x = e.layerX, y = e.layerY;
    var dt = e.dataTransfer, files = dt.files, count = files.length;

    var types = [
            'audio/mp3',
            'audio/mpeg'
    ];

    for (var i=0; i < count; i++) {
    // if (files[i].fileSize < 104857620) 
        var file = files[i];
        var type = file.type;
        var filename = file.fileName;

        if($.inArray(file.type, types) == -1) {
        alert(file.type + 'はサポート外です。');
        continue;
        }

        var reader = new FileReader();
        reader.readAsDataURL(file);
        _upload(file);

        reader.onload = function(e) {
        var fileData = e.target.result;
        _drawImage(x, y, fileData);
        }
   // } else {
     //   alert('ファイルが大きすぎます');
    //}
   }
  };

    var _drawImage = function(x, y, file) {
    var imgElement = document.createElement('img');
    imgElement.src = file;
    imgElement.style.position = 'absolute';
    imgElement.style.display = 'none';
    parent.appendChild(imgElement);

    setTimeout(function(e) {
        var o_w = imgElement.width;
        var o_h = imgElement.height;
        imgElement.width = o_w > 100 ? 100 : o_w;
        imgElement.height = parseInt( o_h * imgElement.width / o_w);

        var w = imgElement.width;
        var h = imgElement.height;
        imgElement.style.left = (x-w / 2)+'px';
        imgElement.style.top = (y-h / 2)+'px';
        imgElement.style.display = 'block';
    },1);
    };

    var _upload = function(file) {
        console.log("upload");

        var fd = new FormData();
        fd.append("xhr2upload", file);
        var xhr = new XMLHttpRequest()
        xhr.open("POST", "http://www.kzfmix.com:5000/upload");
        xhr.send(fd);

        xhr.onload = function(e) {
            var url = e.target.responseText;
            $('#urllists').prepend('<p><a href="' + url + '">'+url+'</a></p>');
            $('#currentimage').html('<img src="' +url+ '">');
        }
    }
}

DnDUploader('dropbox');