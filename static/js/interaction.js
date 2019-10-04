$(document).ready(function() {
    $('.helper-content').hide();
    $('.helper-right > .helper-title').click(function(){
        $('.helper-right > .helper-content').slideToggle();
    });
    $('.helper-left > .helper-title').click(function(){
        $('.helper-left > .helper-content').slideToggle();
    });
});
    

