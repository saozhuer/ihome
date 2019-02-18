$(document).ready(function(){
    $(".auth-warn").show();
})

$(document).ready(function() {
    $.ajax({
        url:'/house/my_house/',
        dataType:'json',
        type:'POST',
        success: function(data){
            if (data.code==200){
                $('.auth-warn').attr('style','display:none')
            }
            if (data.code==1008){
                $('#houses-list').attr('style','display:none')
            }
            console.log(data)
            for (i in data.hlist){
                str = '<li><a href="/house/detail/?house_id='+data.hlist[i].id+'"><div class="house-title">'
                str += '<h3>房屋ID:'+data.hlist[i].id+'—— '+data.hlist[i].title+'</h3>'
                str += '</div><div class="house-content">'
                str += '<img src="'+data.hlist[i].image+'">'
                str += '<div class="house-text"><ul>'
                str += '<li>位于：'+data.hlist[i].area+'</li>'
                str += '<li>价格：￥'+data.hlist[i].price+'/晚</li>'
                str += ' <li>发布时间：'+data.hlist[i].create_time+'</li>'
                str += '</ul></div></div></a></li>'
                $('#houses-list').append(str)
            }
        }
    })

    })

