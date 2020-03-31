window.onload = function(){
    $('.issues-type-header').on('click', function(){
        if(!$('.add-issue-form').is(":visible")){
            $(this).siblings('.issues-list').toggle();
        }
    })

    $('.bookmark-icon').on('click', function(){
        if(!$('.add-issue-form').is(":visible")){
            const project_id = $(this).attr('project-id');
            const selected_project = $(this);
            $.ajax({
                url: '/projects/bookmark_project/',
                data: {
                    'project_id': project_id
                },
                success: function(response){
                    if(response == "project-added"){
                        $(selected_project).html('<i class="fas fa-bookmark"></i>');
                    }else if(response == "project-removed"){
                        $(selected_project).html('<i class="far fa-bookmark"></i>');
                    }else if(response == "redirect"){
                        window.location = "/users/profile/?next=" + window.location.href;
                    }
                }
            })
        }
    })
    $('.project-requests-list-btn').on('click', function(){
        if($('.project-developers-wrapper').is(":visible")){
            $('.project-developers-wrapper').hide();
        }
        if($('.add-issue-form').is(":visible")){
            $('.add-issue-form').hide();
        }
        if(!$('.project-requests-wrapper').is(":visible")){
            $('.project-requests-wrapper').show();
            $('.project-card').addClass('disabled');
        }
    })

    $('.requests-wrapper-close-btn').on('click', function(){
        if($('.project-requests-wrapper').is(":visible")){
            $('.project-requests-wrapper').hide();
            $('.project-card').removeClass('disabled');
        }

    })

    $('.request-btn').on('click', function(){
        const request_code = $(this).attr("request-code");
        const span = $(this).parent().parent().siblings('span');
        const user_id = $(span).attr('user-id');
        const project_id = $(span).attr('project-id');
        $.ajax({
            url: '/projects/handle_pending_project_requests/',
            data: {
                'user_id': user_id,
                'project_id': project_id,
                'request_code': request_code
            },
            success: function(response){
                if(response == 1){
                    $(span).parent().remove();
                }
            }
        })
    })

    $('.project-request-btn').on('click', function(){
        const project_request_btn = $(this);
        const user_id = $(this).attr('user-id');
        const project_id = $(this).attr('project-id');
        $.ajax({
            url: '/projects/handle_project_request/',
            data: {
                'user_id': user_id,
                'project_id': project_id,
            },
            success: function(response){
                if(response == "added"){
                    $(project_request_btn).html("request sent");
                }else if(response == "removed"){
                    $(project_request_btn).html("request cancelled");
                }else{
                    alert(response);
                }
            }
        })
    })

    $('.leave-project-btn').on('click', function(){
        var leave_project = confirm("Sure, you want to leave project?");
        const leave_btn = $(this);
        const user_id = $(this).attr('user-id');
        const project_id = $(this).attr('project-id');
        if(leave_project){
            $.ajax({
                url: '/projects/leave_project_request/',
                data: {
                    'user_id': user_id,
                    'project_id': project_id,
                },
                success: function(response){
                    if(response==1){
                        $(leave_btn).parent().siblings('li').html(
                            '<button class="btn-info btn-sm btn project-request-btn" user-id="' + user_id + '" project-id=" '+ project_id + '">Request</button>'
                        )
                        $(leave_btn).remove();
                        $('.issues').remove();
                    }else{
                        alert('Some error occured while requesting for the project');
                    }
                }
            })
        }
    })

    $('.project-developers-list-btn').on('click', function(){
        if($('.project-requests-wrapper').is(":visible")){
            $('.project-requests-wrapper').hide();
        }
        if($('.add-issue-form').is(":visible")){
            $('.add-issue-form').hide();
        }
        if(!$('.project-developers-wrapper').is(":visible")){
            $('.project-developers-wrapper').show();
            $('.project-card').addClass('disabled');
        }
    })

    $('.developers-wrapper-close-btn').on('click', function(){
        if($('.project-developers-wrapper').is(":visible")){
            $('.project-developers-wrapper').hide();
            $('.project-card').removeClass('disabled');
        }
    })

    $('.add-issue-btn').on('click', function(){
        if($('.project-requests-wrapper').is(":visible")){
            $('.project-requests-wrapper').hide();
        }
        if($('.project-developers-wrapper').is(":visible")){
            $('.project-developers-wrapper').hide();
        }
        if(!$(".add-issue-form").is(":visible")){
            $('.add-issue-form').toggle();
            $('.project-card').addClass('disabled');
        }
    })

    $('.discard-issue-btn').on('click', function(){
        $('.add-issue-form').toggle();
        $('.project-card').removeClass('disabled');
    })

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

    $('.kick-out-btn').on('click', function(){
        var dev_item = $(this).parent('ul').parent('li');
        var dev_name = $(this).attr('data-dev-name');
        var project_id = $(this).attr('data-project-id');
        var dev_id = $(this).attr('data-dev-id');
        var kick_out = confirm('sure want to kick ' + dev_name + ' out of the project?');
        if(kick_out){
            console.log(dev_name);
            console.log(project_id);
            console.log(dev_id);
            $.ajax({
                url: '/projects/kick_out_dev/',
                data: {
                    'dev_id': dev_id,
                    'dev_name': dev_name,
                    'project_id': project_id
                },
                success: function(response){
                    if(response=="removed"){
                        $.when($(dev_item).remove()).then(function(){
                            alert(dev_name + ' successfully removed from the project');
                        });
                    }
                }
            })
        }
    })

    $('.invite-status-btn').on('click', function(){
        if($('.project-requests-wrapper').is(":visible")){
            $('.project-requests-wrapper').hide();
        }
        if($('.add-issue-form').is(":visible")){
            $('.add-issue-form').hide();
        }
        if($('.project-developers-wrapper').is(":visible")){
            $('.project-developers-wrapper').hide();
        }
        if(!$('.invite-status-wrapper').is(':visible')){
            $('.invite-status-wrapper').show();
            $('.project-card').addClass('disabled');
        }
    })

    $('.invites-wrapper-close-btn').on('click', function(){
        $('.invite-status-wrapper').hide();
        $('.project-card').removeClass('disabled');
    })

    $('.cancel-invite').on('click', function(){
        var cancel = confirm('Sure want to cancel invite?');
        if(cancel){
            var parent = $(this).parent('ul').parent('li');
            var user_id = $(this).attr('data-user-id');
            var project_id = $(this).attr('data-project-id');

            $.ajax({
                url: '/projects/cancel_invite/',
                data: {
                    'user_id': user_id,
                    'project_id': project_id
                },
                success: function(response){
                    if(response == "cancelled"){
                        alert('Dev request cancelled successfully');
                        $(parent).remove();
                    }
                }
            })
        }
    })
}