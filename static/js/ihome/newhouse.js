function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

//上传图片后在页面显示图片
 $('#house-image').on('change',function(){
    	var filePath = $(this).val(),         //获取到input的value，里面是文件的路径
    		fileFormat = filePath.substring(filePath.lastIndexOf(".")).toLowerCase(),
    		src = window.URL.createObjectURL(this.files[0]); //转成可以在本地预览的格式

    	// 检查是否是图片
    	if( !fileFormat.match(/.png|.jpg|.jpeg/) ) {
    		error_prompt_alert('上传错误,文件格式必须为：png/jpg/jpeg');
        	return;
        }

        $('#show_image').attr('src',src);
});






$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    $.ajax({
        url:'/house/area_facility/',
        dataType:'json',
        type:'GET',
        success: function(data){
            console.log(data)
            var str =''
            for (i in data.area){
                str +='<option value="'+data.area[i].id+'">'+data.area[i].name+'</option>'
                $('#area-id')[0].innerHTML = str
            }
            $('#form-house-image').attr('style','display:block')
        }
    })



    function show(){
        facility = []
        var obj = document.getElementsByName('facility');
        for (i in obj){
            if (obj[i].checked){
                facility.push(obj[i].value)
            }
        }
    }

    $('#form-house-info').submit(function(e){
        e.preventDefault();
        show()
        $(this).ajaxSubmit({
            url:'/house/new_house/',
            dataType:'json',
            type:'POST',

            success: function(data){
                console.log(data)
                console.log('成功')
                $('#house-id').val(data.house_id)
                alert('发布房源成功！请添加房源图片！')
            },
            error: function(data){
                console.log('失败')
            }

        })
    })

    $('#form-house-image').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/image_house/',
            type:'POST',
            dataType:'json',
            success: function(data){
                alert('图片上传成功')

            },
            error:function(data){
                console.log('error')
            }
        })
    })

})