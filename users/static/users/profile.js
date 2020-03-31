window.onload = function(){
    $('#div_id_first_name').addClass('col-md-6');
    $('#div_id_last_name').addClass('col-md-6');
    $("#div_id_interests").children("div").children('div').addClass("form-check-inline");

    $('.dev-action-btn').on('click', function(){
        var parent = $(this);
        var target = $(this).children('i');
        var user_id = $(target).attr('data-user-id');
        var url = $(target).attr('data-target-url');

        $.ajax({
            url: url,
            success: function(response){
                if(response == "send"){
                    $(parent).html('<i class="fas fa-user-minus mr-2" data-target-url="/users/cancel_dev_request/' + user_id + '/" data-user-id="' + user_id + '"></i>Cancel Request');
                }else if(response == "cancelled"){
                    $(parent).html('<i class="fas fa-user-plus mr-2" data-target-url="/users/send_dev_request/' + user_id + '/" data-user-id="' + user_id + '"></i>Send Request');
                }else if(response == "accepted"){
                    $(parent).siblings('li').remove();
                    $(parent).html('<span><i class="fas fa-user-friends mr-2"></i>Connected</span><i class="fas fa-user-minus ml-3 mr-2" data-target-url="/users/break_connection/' + user_id + '/" data-user-id="' + user_id + '"></i>Break Connection');
                }else if(response == "rejected"){
                    $(parent).siblings('li').remove();
                    $(parent).remove();
                }else if(response == "broke"){
                    $(parent).html('<i class="fas fa-user-plus mr-2" data-target-url="/users/send_dev_request/' + user_id + '/" data-user-id="' + user_id + '"></i>Send Request');
                }
            }
        })
    });
}