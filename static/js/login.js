$(document).ready(function () {
    $('.my-button').click(function () {
        $.post('/login',{phone:$('.phoneInput input').val(),password:$('.passwordInput input').val()},function (data) {
            if(data=='登陆成功')
            {
                window.location.href = "/";
            }
            else {
                $('.warning').text(data);
            }
        })
    })
})