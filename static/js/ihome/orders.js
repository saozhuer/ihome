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
function x(self){
        var orderId = $(self).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
        var h_id = $('.modal-comment').attr('order-id')
        $('.form-control').attr('id','comment'+h_id+'')
    }



function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){


    $.get('/order/all_orders/',function(data){

        console.log(data.all_orders)


        for(i in data.all_orders){
            str = '<li order-id="'+data.all_orders[i].order_id+'"><div class="order-title"><h3 id="order_id">订单编号:'+data.all_orders[i].order_id+'</h3><div class="fr order-operate">'
                    +'<button type="button" class="btn btn-success order-comment'+data.all_orders[i].order_id+'" data-toggle="modal" data-target="#comment-modal" onclick="x(this)">发表评价</button>'
                    +'</div></div><div class="order-content">'
                    +'<img src="'+data.all_orders[i].image+'">'
                    +'<div class="order-text"><h3>订单</h3><ul>'
                    +'<li>创建时间：'+data.all_orders[i].create_date+'</li>'
                    +'<li>入住日期：'+data.all_orders[i].begin_date+'</li>'
                    +'<li>离开日期：'+data.all_orders[i].end_date+'</li>'
                    +'<li>合计金额：'+data.all_orders[i].amount+'元(共'+data.all_orders[i].days+'晚)</li>'
                    +'<li>订单状态：'
                    +'<span>'+data.all_orders[i].status+'</span></li>'
                    +'<li id="pj'+data.all_orders[i].order_id+'" style="display:none">我的评价：'+data.all_orders[i].comment+'</li>'
                    +'<li id="judan'+data.all_orders[i].order_id+'" style="display:none">拒单原因：'+data.all_orders[i].comment+'</li>'
                    +'</ul></div></div></li>'

            $('.orders-list').append(str)



            if(data.all_orders[i].status=='已拒单'){
                $('#judan'+data.all_orders[i].order_id+'').attr('style','display:block')
            }
            if(data.all_orders[i].status!='已完成'){
                console.log(data.all_orders[i].status,i)
                $('.order-comment'+data.all_orders[i].order_id+'').attr('style','display:none')
            }
            if(data.all_orders[i].status=='待支付'){
                 console.log(data.all_orders[i].status,i)
                 $('.order-comment'+data.all_orders[i].order_id+'').html('去支付')
                 $('.order-comment'+data.all_orders[i].order_id+'').attr('style','display:block')
            }
        }




        $(".modal-comment").on("click", function(){
            var h_id = $('.modal-comment').attr('order-id')
            $('.form-control').attr('id','comment'+h_id+'')
            comment = $('#comment'+h_id+'').val()
            order_id = $('.modal-comment').attr('order-id')
            $('#pj'+h_id+'').attr('style','display:block')
            console.log(order_id)

            $.ajax({
            url:'/order/my_order/',
            dataType:'json',
            type:'POST',
            data:{'comment':comment,'order_id':order_id},
            success:function(data){


                location.reload()
            },
            error:function(data){
                console.log('error')
            }
            })
        })

    })
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);





});