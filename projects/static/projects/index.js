window.onload = function(){

    $('.bookmark-icon').on('click', function(){
        if(!$('.new-project-form').is(":visible")){
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

    $('.new-project-btn').on('click', function(){
        if($('.new-project-form').is(':visible')){
            $(this).html('<i class="fas fa-plus"></i>');
        }else{
            $(this).html('<i class="fas fa-times"></i>');
        }
        $(".wrapper").toggleClass('grayed-out');
        $('.new-project-form').toggle();
    })

    $('#id_title').attr('placeholder', 'Enter title for your project');
    
    $('#id_description').attr('placeholder', 'Give a short description about your project');

    $('.urlinput').attr('placeholder', 'Provide git repo link or any other link');

    $('#id_contact').attr('placeholder', 'provide your contact link eg. user@something.com');

    $('#div_id_language').children('div').children('div').addClass("form-check-inline");

    // search projects 
    $("#search-projects-input").on('keyup', function(){
        var value = $(this).val().toLowerCase();
        $(".projects-list li").filter(function(){
            $(this).toggle($(this).children(".project-title").children('h5').text().toLowerCase().indexOf(value) > -1);
        })
    })
}