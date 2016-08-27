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
});