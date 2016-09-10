$( function() {

function create_form(action, method) {
    'use strict';
    var form;
    form = $('<form />', {
        action: action,
        method: method,
        style: 'display: none;'
    });
//    if (typeof input !== 'undefined' && input !== null) {
//        $.each(input, function (name, value) {
//            $('<input />', {
//                type: 'hidden',
//                name: name,
//                value: value
//            }).appendTo(form);
//        });
//    }
    form.appendTo('body').submit();
}

    $("#preloader").hide();
    $('#logout-btn').button();
    $('#logout-btn').click(function(){
        window.location.href = '/logout'
    });
    $('#sync-btn').button();
    $('#pdf-btn').button();
    $('#theme-btn').button();
    $('#usetheme-btn').button();

    $('#sync-btn').click(function(){
        //Start loading GIF
        $("#status").fadeIn();
        $("#preloader").fadeIn();
        console.log('Going to sync');
        $.post('/sync',function(){
            //End loading GIF
            $("#status").fadeOut();
            $("#preloader").fadeOut();
        });
        console.log('Sync Triggered');
    });
    $('#pdf-btn').click(function(){
        console.log('PDF Generation');
        var url = '/pdf'+window.location.pathname;
        $('#downloadFrame').remove(); // This shouldn't fail if frame doesn't exist
        $('body').append('<iframe id="downloadFrame" style="display:none"></iframe>');
        $('#downloadFrame').attr('src',url);
    });
    $('#theme-btn').click(function(){
        var url = '/edit'+window.location.pathname;
        window.location.href = url;
    });

    $('#usetheme-btn').click(function(){
        console.log('Use theme'+window.location.pathname);
//        $.post('/use'+window.location.pathname);
        create_form('/use'+window.location.pathname,'post');
    });



});