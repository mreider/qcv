$( function() {
    $('#logout-btn').button();
    $('#logout-btn').click(function(){
        window.location.href = '/logout'
    });
    $('#sync-btn').button();
});