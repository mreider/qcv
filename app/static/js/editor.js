$(document).ready(function(){
    $("#preloader").hide();
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/html");
    editor1 = ace.edit("editor1");
    editor1.setTheme("ace/theme/monokai");
    editor1.getSession().setMode("ace/mode/css");

    $('#back').button();
    $('#back').click(function(){
        window.location.href = '/'+window.location.pathname.split('/')[2];

    });

    $('#format-css').click(function(){
        console.log('Formatting CSS');
        var beautify = ace.require("ace/ext/beautify");
        beautify.beautify(editor1.session);
    });
    $('#format-html').click(function(){
        console.log('Formatting html');
        var beautify = ace.require("ace/ext/beautify");
        beautify.beautify(editor.session);
    });

    $('#save-btn').click(function(){
        console.log('Submit intercepted');
        var beautify = ace.require("ace/ext/beautify"); // get reference to extension

//        beautify.beautify(editor.session);
//        beautify.beautify(editor1.session);
        var html = editor.getValue();
        var css = editor1.getValue();
        var path =window.location.href = '/'+window.location.pathname.split('/')[2];
        $("#status").fadeIn();
        $("#preloader").fadeIn();

        $.post('/save'+path,{html_content:html,css_content:css},function(data){
            $("#status").fadeOut();
            $("#preloader").fadeOut();
//            window.location.href = '/'+path;
        });
    });
    $('#revert-html').click(function(){
        editor.setValue($('#original-html').val());
    });
    $('#revert-css').click(function(){
        editor1.setValue($('#original-css').val());
    });
});