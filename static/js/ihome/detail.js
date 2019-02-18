function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){

    id = document.location.search
    house_id = id.split('=')[1]


    $.ajax({
        url:'/house/house_detail/',
        type:'GET',
        dataType:'json',
        data:{'house_id':house_id},
        success:function(data){
            console.log(data)
            $('.house-title').html(data.house.title)
            for (i in data.house.images){
                str = '<li class="swiper-slide"><img src="'+data.house.images[i]+'"></li>'
                $('.swiper-wrapper').append(str)
            }

            $('.landlord-pic img').attr('src',data.house.user_avatar)
            $('.landlord-name span').html(data.house.user_name)
            $('#address').html(data.house.address)
            $('.house-price span').html(data.house.price)
            $('#room_count').html('出租'+data.house.room_count+'间')
            $('#acreage').html('房屋面积'+data.house.acreage+'平米')
            $('#unit').html('房屋户型:'+data.house.unit)
            $('#capacity').html('宜住:'+data.house.capacity+'人')
            $('#beds').html(data.house.beds)
            $('#deposit span').html(data.house.deposit)
            $('#min_days span').html(data.house.min_days)
            $('#max_days span').html(data.house.max_days)
            $('.book-house').attr('href','/house/booking/?house_id='+data.house.id+'')
             var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })
            $(".book-house").show();

            if (data.booking=='0'){
//                $('.book-house').attr('style','display:none')
            }


        },
        error:function(data){
            console.log('error')
        }
})

})