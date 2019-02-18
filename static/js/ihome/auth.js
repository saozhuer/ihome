function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function() {
     $.ajax({
            url:'/user/auth_info/',
            dataType:'json',
            type:'GET',
            success: function(data){
                console.log(data)
                $('#real-name').val(data.id_name)
                    $('#id-card').val(data.id_card)
                if (!$('#real-name').val()){
                    $('.btn-success').attr('style','display:block')
                    $('#real-name').removeAttr('disabled')

                    }
                if (!$('#id-card').val()){
                    $('.btn-success').attr('style','display:block')
                    $('#id-card').removeAttr('disabled')

                    }


            }

        })


    $("#form-auth").submit(function(e){
        e.preventDefault();
        real_name = $('#real-name').val()
        id_card = $('#id-card').val()

        if (!real_name){
            $('.error-msg').html('信息填写不完整，请补全信息')
            $(".error-msg").show();
        }
        if (!id_card){
            $('.error-msg').html('信息填写不完整，请补全信息')
            $(".error-msg").show();
        }





        $.ajax({
            url:'/user/auth/',
            dataType:'json',
            type:'POST',
            data:{'real_name':real_name,'id_card':id_card},
            success: function(data){
                if (data.code==200){
                    alert('实名认证成功')
                    location.href = '/user/my/'
                }
                if (data.code==400){
                    console.log('400')
                    $('.error-msg').html('信息填写不完整，请补全信息')
                    $(".error-msg").show();
                }
                if (data.code==1007){
                    console.log('400')
                    $('.error-msg').html('身份证号码错误')
                    $(".error-msg").show();
                }
            },
            error: function(data){
                console.log('失败')
            }

        })
        })
    })

