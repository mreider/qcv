$( function() {
    $('#logout-btn').button();
    $('#logout-btn').click(function(){
        window.location.href = '/logout'
    });
    $('#sync-btn').button();
    $('#pdf-btn').button();

    $('#sync-btn').click(function(){
        //Start loading GIF
        console.log('Going to sync');
        $.post('/sync',function(){
            //End loading GIF
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
});