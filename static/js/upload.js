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
        var fd = new FormData();
        fd.append("xhr2upload", file);
        var xhr = new XMLHttpRequest()
        xhr.open("POST", "http://localhost:5000/user/generate");
        xhr.send(fd);
    }
}

DnDUploader()