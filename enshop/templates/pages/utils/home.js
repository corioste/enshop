let perPage = 5;

(function() {
	window.onresize = displayWindowSize;
	window.onload = displayWindowSize;
  
	function displayWindowSize() {
	  let myWidth = window.innerWidth;
	  console.log(myWidth)
	  // your size calculation code here
		if(myWidth < 791){
			perPage =1;
			new Splide( '#splide', {
				type   : 'loop',
				perPage: perPage,
				perMove: 1,
				pagination: false,
				autoplay: true
			} ).mount();
		}else{
			perPage = 5
			new Splide( '#splide', {
				type   : 'loop',
				perPage: perPage,
				perMove: 1,
				pagination: false,
				autoWidth: true,
				autoplay: true
			} ).mount();
		}
	};
})()

new Splide( '#splide', {
	type   : 'loop',
	perPage: perPage,
	perMove: 1,
	pagination: false,
	autoplay: true
} ).mount();
  
  