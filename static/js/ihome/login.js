function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }

//        异步请提交登陆请求
        $.ajax({
            url: "/user/login/",
            type: "POST",
            dataType: "json",
            data:{'mobile':mobile,'password':passwd,},
            success: function(data){
               if (data.code=='1001'){
                   $("#mobile-err span").html("该用户不存在");
                   $("#mobile-err").show();
              }
               if (data.code=='1002') {
                    $("#password-err span").html("密码不正确!");
                    $("#password-err").show();
               }
               if (data.code=='1003'){
                   $("#mobile-err span").html("手机号码格式不正确");
                   $("#mobile-err").show();
              }
              if (data.code=='200'){
                location.href = '/user/my/'
              }
            },
            error: function(data){
                alert('error')
             }
        });

    });
})