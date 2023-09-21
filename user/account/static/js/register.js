$(document).ready(function () {
    var $password = $("#password");
    var $confirmPassword = $("#confirm-password");
    
    var $submitButton = $("input[type='submit']");

    $password.add($confirmPassword).on("keyup", function () {
        var password = $password.val();
        var confirmPassword = $confirmPassword.val();
        
        if (confirmPassword === "") {
            $("#password-match").text("");
        } else {
            if (password === confirmPassword) {
                $("#password-match").text("");
                $submitButton.prop("disabled", false);
            } else {
                $("#password-match").text("パスワードが一致していません。");
                $submitButton.prop("disabled", true);
            }
        }
    });
});