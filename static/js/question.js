$(document).ready(function () {
    $('.li-question').addClass('active');
    $('textarea').autosize();
    $('.my-button').click(sendMessage);
})

function sendMessage() {
    title = $('.Input-title').val();
    context = $('.Input-context').val()
    if(judgeTitle())
    {
        $.post('/question',{'title':title,'context':context},function (data) {
            if(data=='提交成功')
            {
                window.location.href = "/";
            }
            else {
                $('.warning').text(data);
            }
        })
    }
}

function judgeTitle() {
    title = $('.Input-title').val();
    if(title.length<=10)
    {
        $('.warning').text('问题太短了，详细一点呀');
        return false;
    }
    return true;
}

