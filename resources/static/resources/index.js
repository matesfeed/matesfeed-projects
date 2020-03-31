window.onload = function(){
    $('#div_id_tag').children('div').children('div').addClass("form-check-inline");

    $('.bookmark-icon').on('click', function(){
        if(!$('.add-resource-form').is(":visible")){
            const resource_id = $(this).attr('resource-id');
            const selected_resource = $(this);
            $.ajax({
                url: '/resources/bookmark_resource/',
                data: {
                    'resource_id': resource_id
                },
                success: function(response){
                    if(response == "resource-added"){
                        $(selected_resource).html('<i class="fas fa-bookmark ml-2"></i>');
                    }else if(response == "resource-removed"){
                        $(selected_resource).html('<i class="far fa-bookmark ml-2"></i>');
                    }else if(response == "redirect"){
                        window.location = "/users/profile/?next=" + window.location.href;
                    }
                }
            })
        }
    })

    $('.add-resource-btn').on('click', function(){
        if($('.add-resource-form').is(':visible')){
            $(this).html('<i class="fas fa-plus"></i>');
            $('.wrapper').removeClass('grayed-out');
        }else{
            $(this).html('<i class="fas fa-times"></i>');
            $('.wrapper').addClass('grayed-out');
        }
        $('.add-resource-form').toggle();
        
    })

    $("#search-resources-input").on('keyup', function(){
        var value = $(this).val().toLowerCase();
        $("#resources-list li").filter(function(){
            $(this).toggle($(this).children("h4").text().toLowerCase().indexOf(value) > -1);
        })
    })

    $('.add-resource-to-project-icon').on('click', function(){
        if($('.add-resource-form').is(":visible")){
            $('.add-resource-form').hide();
        }
        $('.wrapper').addClass('grayed-out');

        var resource_id = $(this).attr('data-resource-id');
        $('.add-resource-to-project-wrapper').show("fast", function(){
            $('.add-resource-to-project-btn').on('click', function(){
                var project_id = $(this).attr('data-project-id');
        
                $.ajax({
                    url: '/resources/add_resource_to_project/',
                    data: {
                        'project_id': project_id,
                        'resource_id': resource_id
                    },
                    success: function(response){
                        $('.add-resource-to-project-wrapper').hide(function(){
                            $('.wrapper').removeClass('grayed-out');
                            alert(response);
                        })
                    }
                })
            })
        });
    })

    $('.remove-resource-from-project-icon').on('click', function(){
        var remove_btn = $(this);
        var remove = confirm('You sure want to remove this resource');
        var resource_id = $(this).attr('data-resource-id');
        var project_id = $(this).attr('data-project-id');
        if(remove){
            $.ajax({
                url: '/resources/remove_resource_from_project/',
                data: {
                    'project_id': project_id,
                    'resource_id': resource_id
                },
                success: function(response){
                    if(response=="removed"){
                        $.when($(remove_btn).parent('ul').parent('.resource-item').remove()).then(function(){
                            alert('Resource successfully removed');
                        });
                    }else if(response==0){
                        alert('If you really want to test django skills please contact at 8327543222');
                    }else{
                        alert('Something went wrong.Please try refreshing the page');
                    }
                }
            })
        }
    })

    $('.close-add-resource-to-project-btn').on('click', function(){
        $('.wrapper').removeClass('grayed-out');
        $('.add-resource-to-project-wrapper').hide();
    })

    
}