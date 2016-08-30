$(document).ready(function(){
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/html");
    editor1 = ace.edit("editor1");
    editor1.setTheme("ace/theme/monokai");
    editor1.getSession().setMode("ace/mode/css");

    $('#back').button();
    $('#back').click(function(){
        window.location.href = '/'+window.location.pathname.split('/')[2]
        e;
    });
});