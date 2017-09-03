$(document).ready(function(){
    $("#testimonial-slider").owlCarousel({
        items: 1,
        itemsDesktop:[1000,1],
        itemsDesktopSmall:[979,1],
        itemsTablet:[768,1],
        pagination: true,
        loop:true,
        autoplay: true,
        autoplaySpeed: 2000,
        autoplayHoverPause: true
    });
});