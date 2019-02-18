function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){



    id = document.location.search
    house_id = id.split('=')[1]

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

    $.ajax({
        url:'/house/house_booking/',
        dataType:'json',
        type:'GET',
        data:{'house_id':house_id},
        success:function(data){
            console.log(data)

            $('#title').html(data.house.title)
            $('#price span').html(data.house.price)
            $('#image').attr('src',data.house.image)


        },
        error:function(data){
            console.log('error')
        }
    })

    $('.submit-btn').click(function(){
        begin_date = $('#start-date').val()
        end_date = $('#end-date').val()

        $.ajax({
            url:'/order/create_order/',
            dataType:'json',
            type:'POST',
            data:{'hosue_id':house_id,'begin_date':begin_date,'end_date':end_date},
            success:function(data){

                if (begin_date && end_date){
                location.href = '/order/my_order/'
                }else{
                    alert('请选择入住时间')
                }
            },
            error:function(data){
                console.log('error')
            }
        })

    })




})
