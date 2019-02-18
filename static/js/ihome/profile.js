function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

//上传图片后在页面显示图片
$("#img_input").change(function(){
$("#user-avatar").attr("src",URL.createObjectURL($(this)[0].files[0]));
});


$(document).ready(function() {
    $('#form-avatar').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            type: 'PATCH',
            url: '/user/profile/',
            dataType: 'json',
            success:function(data){
                 console.log('success')
            },
            error : function() {
              alert("操作失败");
            }
    })
    })
    $('#form-name').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            type: 'PATCH',
            url: '/user/profile/',
            dataType: 'json',
            success:function(data){
                 location.href = '/user/my/'
            },
            error : function() {
              alert("操作失败");
            }
    })
    })

    })

