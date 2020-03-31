window.onload = function(){
    $('.handle-request').on('click', function(){
        var parent = $(this);
        var url = $(parent).children('i').attr('data-target-url');
        var user_id = $(parent).children('i').attr('data-dev-id');
        $.ajax({
            url: url,
            success: function(response){
                if(response == "added"){
                    $(parent).html('<i class="fas fa-user-minus mr-2" data-target-url="/users/cancel_dev_request/' + user_id + '/" data-dev-id="' + user_id + '"></i>Cancel Request');
                }else if(response=="accepted"){
                    $(parent).siblings('li').remove();
                    $(parent).html('<li class="list-inline-item"><i class="fas fa-user-friends mr-2"></i>Connected</li><li class="list-inline-item handle-request"><i class="fas fa-user-times mr-2" data-target-url="/users/break_connection/' + user_id + '/" data-dev-id="' + user_id + '"></i>Break Connection</li>');
                }else if(response=="cancelled"){
                    $(parent).html('<i class="fas fa-user-times mr-2" data-target-url="/users/accept_dev_request/' + user_id + '/" data-dev-id="' + user_id + '"></i>Send Request');
                }else if(response=="broke"){
                    $(parent).siblings('li').remove();
                    $(parent).html('<i class="fas fa-user-times mr-2" data-target-url="/users/send_dev_request/' + user_id + '/" data-dev-id="' + user_id + '"></i>Send Request');
                }else if(response=="rejected"){
                    $(parent).parent('ul').parent('li').remove();
                }else if(response=="send"){
                    $(parent).html('<i class="fas fa-user-minus mr-2" data-target-url="/users/cancel_dev_request/' + user_id + '/" data-dev-id="' + user_id + '"></i>Cancel Request');
                }
            }
        })
    })
}