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
        var dt = e.dataTransfer, files = dt.files, count = files.length;

        var types = [
            'audio/mp3',
            'audio/mpeg',
            'audio/wav',
        ];

        if (files[0].size < 1048576) {
            var file = files[0];
            var type = file.type;

            if ($.inArray(file.type, types) == -1) {
                alert(file.type + 'はサポート外です。');
            } else {
                _upload(file);
            }
        } else {
            alert('ファイルが大きすぎます');
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