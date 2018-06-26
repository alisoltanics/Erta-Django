
$(document).ready(function(){


  $(function(){

    $('.container .slides:gt(0)').hide();
    setInterval(function(){
      $('.container :first-child').fadeOut(-222222222222).next('.slides').fadeIn()
      .end().appendTo('.container');
  }, 5000);

  });

});

$(document).ready(function(){

  $(function(){

$("#hmenu").click(function(){
    $("#mynv").toggleClass("nv1");
});

});

});




$(document).ready(
 function() {
 setInterval(function() {
      $("#pms").load(window.location.href + " #pms", "");
 }, 30000);  //Delay here = 5 seconds

});
