var DnDUploader = function () {
    var __body = document.getElementsByTagName('body')[0];
    var parent = document.getElementById('drop-area');
    __body.addEventListener("drop", function (e) { e.stopPropagation(); e.preventDefault(); }, false);
    __body.addEventListener("dragenter", function (e) { e.stopPropagation(); e.preventDefault(); }, false);
    __body.addEventListener("dragover", function (e) { e.stopPropagation(); e.preventDefault(); }, false);
    parent.addEventListener("drop", function (e) { e.stopPropagation(); e.preventDefault(); _handleDrop(e); }, false);
    parent.addEventListener("dragenter", function (e) { e.stopPropagation(); e.preventDefault(); }, false);
    parent.addEventListener("dragover", function (e) { e.stopPropagation(); e.preventDefault(); }, false);

    var _handleDrop = function (e) {
        var files = e.dataTransfer.files;
        var fr = new FileReader();
        fr.readAsDataURL(files[0]);
        document.getElementById('loading-screen').style.display = 'block';
        // check file extension
        var types = [
            'audio/mp3',
            'audio/mpeg',
            'audio/wav',
        ];

        fr.onload = function (e) {
            var file = e.target.result;
            var type = file.split(';')[0].split(':')[1];
            if (types.indexOf(type) < 0) {
                alert('File type not supported');
                return;
            }

            _upload(files[0]);
        }
    };

    var _upload = function (file) {       
        var hidden_id = document.getElementById('user_id')
        var id = hidden_id.value;
        var fd = new FormData();
        fd.append("xhr2upload", file);
        var xhr = new XMLHttpRequest()
        xhr.open("POST", "http://localhost:5000/user/generate/"+id);
        console.log("http://localhost:5000/user/generate/"+id);
        xhr.send(fd);
        xhr.onload = function () {
            document.getElementById('loading-screen').style.display = 'none';
            alert("画像の生成に成功しました");
        };
    }
}

DnDUploader()