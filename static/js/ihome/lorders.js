//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
function x(self){
        var orderId = $(self).parents("li").attr("order-id");
        $(".modal-accept").attr("order-id", orderId);
    }

function y(self){
        var orderId = $(self).parents("li").attr("order-id");
        $(".modal-reject").attr("order-id", orderId);
    }


$(document).ready(function(){


    $.get('/order/my_lorders/',function(data){
        console.log(data.olist)
        for(i in data.olist){
            str = '<li  order-id="'+data.olist[i].order_id+'"><div class="order-title"><h3 id="order_id">订单编号:'+data.olist[i].order_id+'</h3><div class="fr order-operate">'
                    +'<div class="fr order-operate'+data.olist[i].order_id+'">'
                    +'<button type="button" class="btn btn-success order-accept" data-toggle="modal" data-target="#accept-modal" onclick="x(this)">接单</button>'
                    +'<button type="button" class="btn btn-danger order-reject" data-toggle="modal" data-target="#reject-modal" onclick="y(this)">拒单</button></div>'
                    +'</div></div><div class="order-content">'
                    +'<img src="'+data.olist[i].image+'">'
                    +'<div class="order-text"><h3>订单</h3><ul>'
                    +'<li>创建时间：'+data.olist[i].create_date+'</li>'
                    +'<li>入住日期：'+data.olist[i].begin_date+'</li>'
                    +'<li>离开日期：'+data.olist[i].end_date+'</li>'
                    +'<li>合计金额：'+data.olist[i].amount+'元(共'+data.olist[i].days+'晚)</li>'
                    +'<li>订单状态：'
                    +'<span>'+data.olist[i].status+'</span></li>'
                    +'<li id="pj'+data.olist[i].order_id+'" style="display:none">客户评价：'+data.olist[i].comment+'</li>'
                    +'<li id="judan'+data.olist[i].order_id+'" style="display:none">拒单原因：'+data.olist[i].comment+'</li>'
                    +'</ul></div></div></li>'

            $('.orders-list').append(str)

            if(data.olist[i].status=='已拒单'){
                $('#judan'+data.olist[i].order_id+'').attr('style','display:block')
            }
            if(data.olist[i].status!='待接单'){
                $('.order-operate'+data.olist[i].order_id+'').attr('style','display:none')
            }
            if(data.olist[i].status=='已完成'){
                $('#pj'+data.olist[i].order_id+'').attr('style','display:block')
            }





        }

    })

    $('.modal-accept').click(function(){
        od = $(this).attr('order-id')
        $('.order-text li span').html('待支付')
        orders_status = $('.order-text li span').html()

        location.reload()

        $.ajax({
            url:'/order/orders_status/',
            type:'POST',
            dataType:'json',
            data:{'order_id':od,'orders_status':orders_status},
            success:function(data){
                console.log(data)
            },
            error:function(data){
                console.log('error')
            }
        })

    })
    $('.modal-reject').click(function(){
        od = $(this).attr('order-id')
//        $('#reject-reason').attr('id','reject-reason'+od+'')
        $('.order-text li span').html('已拒单')
        orders_status = $('.order-text li span').html()
        comment = $('#reject-reason').val()
        console.log(comment)
        location.reload()
        $.ajax({
            url:'/order/orders_status/',
            type:'POST',
            dataType:'json',
            data:{'order_id':od,'orders_status':orders_status,'comment':comment},
            success:function(data){
                console.log(data)
            },
            error:function(data){
                console.log('error')
            }
        })



    })


    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-accept").on("click", function(){
        console.log('aaa')
        var orderId = $(this).parents("li").attr("order-id");
        console.log(this)
        $(".modal-accept").attr("order-id", orderId);
    });
    $(".order-reject").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-reject").attr("order-id", orderId);
    });

});