$(document).ready(function(){
    // перезагрузка при нажатии кнопки назад в браузере
    $.ajaxSetup({ cache: false });
    window.onpopstate = function(event) {
        if(event && event.state) {
            location.reload()
        }
    }


    // dataColor будем использовать при отрисовке добавленного продукта
     dataColor={
                5: 'Любой',
                4: 'Индийское дерево',
                3: 'Венге',
                2: 'Бронза',
                1: 'Белый',

            };

//Удаление позиции в малой корзине
    $('.new-products-list-in-basket tbody').on('click','input.del-product-item',function(){
        event.preventDefault();

        var product_id = $(this).data('product_id');
        var url = $(this).data('url_action');
        var product_color_id = $(this).data('product_color_id');
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();

        var data = {};
        data.product_id = product_id;
        data.product_color_id = product_color_id;
        data['csrfmiddlewaretoken'] = csrf;


        $.ajax({
            url:url,
            type:'POST',
            data:data,
            success:function(data){
                console.log('OK');

                $(".basket_total_nmb").text(data['nmb_after_delete']);
                var list_products_in_small_basket = JSON.parse(data['last_adding_product']);
                var newLine = ''
                for (const [key, value] of Object.entries(list_products_in_small_basket)) {


                                        newLine = newLine +'<tr class="miniCartProduct ">'+
                                    '<td style="width:20%" class="miniCartProductThumb">'+
                                        '<div><img src=\"/media'+value['fields']['image']+'\" alt="img"></div></td><td style="width:35%">'+
                                        '<div class="miniCartDescription">'+
                                            '<h4><a href="">' +value['fields']['product_name']+ '</a></h4></div>'+
                                    '</td><td style="width:15%"><div'+
                                        'class="miniCartDescription"><h4><a href="">' +dataColor[value['fields']['color']]+
                                        '</a></h4></div></td>'+
                                    '<td style="width:15%" class="miniCartQuantity"><a> ' +value['fields']['nmb']+ ' шт. </a></td>'+
                                    '<td style="width:15%" class="miniCartSubtotal"><span> ' +value['fields']['total_price']+ '</span></td>'+
                                    '<td style="width:5%"'+
                                        ' class="delete"><b><input type="button" '+
                                        ' id=\"del-product-item-'+value['pk']+value['fields']['color']+'\"'+
                                        ' class=\"del-product-item\" value=\"х\"'+

                                        " data-product_id="+value['fields']['product']+
                 ' data-url_action="/orders/delete_position/"' +

                  ' data-product_color_id='+ value["fields"]["color"]+

                                        ' </b></td></tr>'

                };

                $('.basket-total-price').html('Общая сумма: '+ data['basket_total_price']+'.00 руб.');
                $('.new-products-list-in-basket tbody').html(newLine);

            },
            error:function(){
                console.log('BAD');
            },
        });



    });
// Добавление позиции в малую корзину
    $(document).on('click','button',function(e){
        event.preventDefault();

        var form_id = $(this).data('form_id'); //получение id формы
        var form = $('#'+form_id); //получение формы

        var product_nmb = $('#'+form_id+ ' input:eq(1)').val(); // получим значение из второго input

        // проверка поля на число
        if (parseInt( product_nmb )<=0){
            $('#'+form_id+ ' input:eq(1)').val('1');
        }else{
            var product_color = $('#'+form_id+'  select option:selected').val(); //выбор цвета
            var url = $(form).attr('action'); //получение  атрибута формы 'action'
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();
            var product_image = $(this).data('product_image').replace('/media', '');
            var product_id = $(this).data('product_id');
            var product_name = $(this).data('product_name');
            var product_price = $(this).data('product_price');
            console.log(product_price)

            var data = {};
            data.product_name = product_name;
            data.product_id = product_id;
            data.product_nmb = product_nmb;
            data.product_price = product_price;
            data.product_color =  product_color;
            data['csrfmiddlewaretoken'] = csrf;
            data.product_image = product_image

            $.ajax({
                url:url,
                type:'POST',
                data:data,
                success:function(data){
                    console.log('OK');

                    $(".basket_total_nmb").text(data['product_total_nmb']);
                    var list_products_in_small_basket = JSON.parse(data['last_adding_product']);
                    var basket_total_price = JSON.parse(data['basket_total_price']);

                    var newLine = ''
                    for (const [key, value] of Object.entries(list_products_in_small_basket)) {


                                            newLine = newLine +'<tr class="miniCartProduct ">'+
                                        '<td style="width:20%" class="miniCartProductThumb">'+
                                            '<div><img src=\"/media'+value['fields']['image']+ '\" alt="img"></div></td>'+
                                            '<td style="width:35%">'+
                                            '<div class="miniCartDescription">'+
                                                '<h4><a href="">' +value['fields']['product_name']+ '</a></h4></div>'+
                                        '</td><td style="width:15%">'+
                                            '<div class="miniCartDescription"><h4><a href="">' +dataColor[value['fields']['color']]+
                                            '</a></h4></div></td>'+
                                        '<td style="width:15%" class="miniCartQuantity"><a> ' +value['fields']['nmb']+ ' шт. </a></td>'+
                                        '<td style="width:15%" class="miniCartSubtotal"><span> ' +value['fields']['total_price']+ '</span></td>'+
                                        '<td style="width:5%"'+
                                            ' class="delete"><b><input type="button" '+
                                            ' id=\"del-product-item-'+value['pk']+value['fields']['color']+'\"'+
                                            ' class=\"del-product-item\" value=\"х\"'+

                                            " data-product_id="+value['fields']['product']+
                     ' data-url_action="/orders/delete_position/"' +

                      ' data-product_color_id='+ value["fields"]["color"]+

                                            ' </b></td></tr>'

                    };

                    $('.basket-total-price').html('Общая сумма: '+ data['basket_total_price']+'.00 руб.');


                    $('.new-products-list-in-basket tbody').html(newLine);

                    $('#'+form_id+ ' input:eq(1)').val('1');


                },
                error:function(){
                    console.log('BAD');
                },
            });
        }

    });
    //пересчет стоимости в большой корзине в зависимости от количества
    $(document).on('change','.quanitySniper',function(e){
        event.preventDefault();
        var products_quantity = $('#'+this.id).val(); //получаем значение из поля количество


        var product_price_str = $(this).parent().parent().find('.pro-pr').html();
        var price_product_float = parseFloat(product_price_str.substr(0, product_price_str.indexOf('.')))
        var total_price = (price_product_float * products_quantity).toFixed(2) // Общая цена позиции

        var product_total_price = $(this).parent().next().text(total_price); // вносим общую цену позиции
        $("#"+this.id).blur(); // снимим фокус с поля ввода количества
        var common_price_arr = $('.total-price-line').text();
        common_price_arr = common_price_arr.split('.00');
        let sumNum = 0;
        for (let n = 0; n < common_price_arr.length; n++) {
            sumNum += +(common_price_arr[n]);
        }
        // общая цена в правом сайтбаре
        var common_price = $('#common_price').text(parseFloat(sumNum).toFixed(2));
        // data атрибуты

         var product_id = $(this).data('product_id');
        var product_color_id = $(this).data('product_color_id');
        var product_nmb = $(this).attr('value','products_quantity');

        var csrf =  $(this).data('csrf');
        var url = $(this).data('url_action');


         var data = {};
        data.product_id = product_id;
        data.product_nmb = products_quantity;
        data.product_color_id = product_color_id;

        data['csrfmiddlewaretoken'] =  csrf;



         $.ajax({
            url:url,
            type:'POST',
            data:data,
            success:function(data){
                console.log('OK');

                },
            error:function(){
                console.log('BAD');
            },
        });
    });


//Удаление позиции в большой корзине
    $('.new-products-list-in-basket tbody').on('click','.delete-position',function(){
        event.preventDefault();
        var product_id = $(this).data('product_id');
        var product_color_id = $(this).data('product_color_id');
        var csrf =  $(this).data('csrf');
        var url = $(this).data('url_action');

        var data = {};
        data.product_id = product_id;
        data.product_color_id = product_color_id;
        data['csrfmiddlewaretoken'] =  csrf;

         $.ajax({
            url:url,
            type:'POST',
            data:data,
            success:function(data){
                console.log('OK');
                var list_products_in_big_basket = JSON.parse(data['last_adding_product']);
                var basket_total_price = data['basket_total_price'];

                var csrf = data['csrf'];

//                console.log(csrf)
//                console.log(list_products_in_big_basket)
                var newl = ''
                for (const [key, value] of Object.entries(list_products_in_big_basket)) {


                                        newl = newl +'<tr class="CartProduct">'+
                                '<td class="CartProductThumb">'+
                                    '<div><a href="product-details.html"><img src=\"/media'+value['fields']['image']+'\" alt="img"></a>'+
                                    '</div>'+
                                '</td>'+
                                '<td>'+
                                    '<div class="CartDescription">'+
                                        '<h4><a href="product-details.html" class="product-name">'+value['fields']['product_name']+ ' </a></h4>'+

                                        '<span class="color">'+dataColor[value['fields']['color']]+'</span>'+

                                        '<div class="price"><span class="pro-pr">'+value['fields']['price_per_item']+' руб.</span></div>'+

                                    '</div>'+
                                '</td>'+
                                '<td'+
                                       ' class="delete"><a title="Удалить всю позицию" class="delete-position"'+
                                "data-product_id = "+value['fields']['product']+
                                " data-product_color_id = "+value['fields']['color']+
                                ' data-url_action="/orders/delete_position_basket/"' +
                                'data-csrf=\"'+data['csrf']+'\">'+

                                    '<i class="glyphicon glyphicon-trash fa-2x"></i></a></td>'+

                                '<td><input class="quanitySniper" type="text" value=\"'+ value["fields"]["nmb"]+'\" name="quanitySniper"'+
                                           'id="quanitySniper_'+value['pk']+'_'+ value["fields"]["color"]+'\"'+
                                ' data-product_id=\"'+value['fields']['product']+'\"'+
                                     ' data-product_color_id=\"'+ value["fields"]["color"]+'\"'+
                                           "data-url_action='/orders/show_basket/'"+

                                'data-csrf=\"'+data['csrf']+'\"'+
                               '</td>'+

                                '<td class="price total-price-line">'+value['fields']['total_price']+'</td>'
                            '</tr>'

                };
                if (data['basket_total_price'] > 0){
                    $('#common_price').html(data['basket_total_price']+'.00 руб.');
                }else{
                    $('#common_price').html('0');
                }

                $('.new-products-list-in-basket tbody:last-child').html(newl); // отрисовываем измененный список товаров


                },
            error:function(){
                console.log('BAD');

            },
        });
    });

});