$(document).ready(function () {
    $('.btn').click(function (e) {
        e.preventDefault();
        key = $('.form-control').val();
        window.location.href = '/search?key='+key;
    })
})