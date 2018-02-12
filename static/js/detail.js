$(document).ready(function () {
    $('textarea').autosize();
    $('.my-button').click(sendMessage);
})

function sendMessage() {
    context = $('textarea').val()
    question_id = window.location.pathname.split('/')[2]
    if(judgeTitle())
    {
        $.post('/answer',{'context':context,'question_id':question_id},function (data) {
            if(data=='提交成功')
            {
                $('.warning').text('回答成功');
                setTimeout(function(){location.reload();},1000);
            }
            else {
                $('.warning').text(data);
            }
        })
    }
}

function judgeTitle() {
    context = $('textarea').val()
    if(context.length<=0)
    {
        $('.warning').text('回答太短了，详细一点呀');
        return false;
    }
    return true;
}
