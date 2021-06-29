$(function() {
    $('.clickMore').on('click', function() {
        $('.showMore').stop().css('display','block').hide().slideDown();
    });
});

$(function() {
    $('.close-search').on('click', function() {
        $('.showMore').stop().css('display','hidden').show().slideToggle();
    });
});
$(function() {
    $('.handle-search').on('click', function() {
       document.forms['search-form'].submit()
    });
});

  

$(document).click(function(event) {
    var value =  $('.showMore').css('display')
    if(value == "none"){
        return
    }
    const flyoutEl = document.getElementsByClassName("showMore")[0];
    const notAllowed = document.getElementsByClassName("clickMore")[0];
    let targetEl = event.target; 
    do {
        if(targetEl==notAllowed){
            return
        }
        if(targetEl == flyoutEl) {
      
          return
        }

        targetEl = targetEl.parentNode;
      } while (targetEl);
    
    $('.showMore').stop().css('display','hidden').show().slideToggle();
});