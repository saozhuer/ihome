function logout() {
    $.get("/user/logout", function(data){
        console.log(data)
        if (data.code=='200') {

            location.href = "/house/index/";
        }
    })
}




$(document).ready(function(){
    $.ajax({
        url:'/user/my_info/',
        dataType:'json',
        type:'GET',
        success: function(data){
        console.log(data)
            $('#user-name').html(data.data.name)
            $('#user-mobile').html(data.data.phone)
            $('#user-avatar').attr('src',data.data.avatar)
            $('#my_auth a').attr('href','/user/auth/')

        }
    })

   })