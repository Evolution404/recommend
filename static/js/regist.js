$(document).ready(function () {
    $('.my-button').click(sendMessage);
})


function sendMessage() {

    if(judge())
    {
        $.post('/regist',{phone:$('.phoneInput input').val(),username:$('.usernameInput input').val(),password:$('.passwordInput input').val()},function (data) {
            if(data == '注册成功') {

                window.location.href='/login';}
                else {
                $('.warning p').text(data);
            }
        })
    }

}

function judge() {
    if(judgePhone())
    {
        if(judgeUsername())
        {
            if(judgePassword())
            {
                return true;
            }
        }
    }
    return false
}

function judgePhone() {
    phone = $('.phoneInput input').val()
    phone=phone.replace(/(^\s*)|(\s*$)/g, "");
    var verify=new RegExp(/^1\d{10}$/);
    if(verify.test(phone))
    {
        $('.warning p').text('');
        return true;
    }
    else {
        $('.warning p').text('请输入正确的手机号');
        return false;
    }
}


function judgeUsername() {
    username = $('.usernameInput input').val();
    if(username.length<=3)
    {
        $('.warning p').text('用户名长度不能小于4');
        return false;
    }
    else if(username.length>=30)
    {
        $('.warning p').text('用户名长度不能大于30');
        return false;
    }
    $('.warning p').text('');
    return true;
}


function judgePassword() {
    password = $('.passwordInput input').val();
    if(password.length<6)
    {
        $('.warning p').text('密码长度不能小于6');
        return false;
    }
    else if(username.length>=64)
    {
        $('.warning p').text('密码长度不能大于64');
        return false;
    }
    $('.warning p').text('');
    return true;
}