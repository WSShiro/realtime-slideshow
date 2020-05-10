/*! 
* script.js
* 
* realtime-slideshow | MIT lincese | https://github.com/WSShiro/realtime-slideshow/blob/master/LICENSE
*/

/////////////////
//		Swiper setting
 ////////////////
// 1st Swiper
var mySwiper1 = new Swiper('.swiper1', {
	effect: 'coverflow',
	initialSlide: 0,
	slidesPerView: 1.5,
	speed: 4000,
	slidesPerGroup: 1,
	loop: false,
	centeredSlides: true,
	spaceBetween: 0,
	freeMode: false,
	scrollbar: {
		el: '.scrollbar1',
		hide: true,
		draggable: true
	},
	autoplay: {
		delay: 1000,
		stopOnLastSlide: false,
		disableOnInteraction: false,
		reverseDirection: false
	},
	on: {
		init: function () {/* do something */}
    },
});
 // 2nd Swiper
var mySwiper2 = new Swiper('.swiper2', {
	spaceBetween: 0,
	initialSlide: 0,
	slidesPerView: 8,
	slidesPerGroup: 1,
	loop: false,
	centeredSlides: true,
	spaceBetween: 3,
	freeMode: false,
	/*navigation: {
		nextEl: '.next2',
		prevEl: '.prev2'
	},*/
	scrollbar: {
		el: '.scrollbar2',
		hide: true,
		draggable: true
	},
	/*controller: {
		control: mySwiper1,
		inverse: false,
		by: 'slide'
	},*/
});
//mySwiper2.controller.control = mySwiper1;

///////////////////
//		image update
//////////////////
var slide_max = 62;
var jsonfile1 = 'image.json';
var jsonfile2 = 'image_display.json';
var jsonimage = [];
var jsonimage_disp = [];
var count = 0;
mySwiper1.on('autoplay', function () {
	// Read json
	httpObj1 = new XMLHttpRequest();
	httpObj1.open("get", jsonfile1, true);
	httpObj1.onload = function(){
		jsonimage = JSON.parse(httpObj1.responseText);
	};
   httpObj1.send(null);
   
   // Add new image
   var num_new = jsonimage.length - jsonimage_disp.length;
   //console.log(count);
   //console.log(num_new);
	if (num_new > 0){
		for (var i=0; i<num_new; i++){
			console.log(jsonimage[num_new - i - 1].href);
			mySwiper1.prependSlide('<div class="swiper-slide slide1"><img src="' + jsonimage[num_new - i - 1].href + '"><div class="slidetitle"><p>Posted by <b>' + jsonimage[num_new - i - 1].title + '</b></p></div></div>');
			mySwiper2.prependSlide('<div class="swiper-slide slide2"><img src="' + jsonimage[num_new - i - 1].href + '"></div>');
		}
		if ( mySwiper1.slides.length > slide_max) {
		//console.log(mySwiper1.slides.length);
		var remove_num = mySwiper1.slides.length - slide_max;
			for (var i=0; i< remove_num ; i++){
				mySwiper1.removeSlide(mySwiper1.slides.length - 3);
				mySwiper2.removeSlide(mySwiper2.slides.length - 3);
			}			
		}
		//console.log(mySwiper1.slides.length);
		mySwiper1.update();
		mySwiper2.update();
		mySwiper1.slideTo(0, 400 * mySwiper1.realIndex, false);  //(index, speed(ms), runCallbacks)
		mySwiper2.slideTo(0, 400 * mySwiper2.realIndex, false);  //(index, speed(ms), runCallbacks)
		jsonimage_disp = jsonimage;
		count++;
	}
	
});
 
///////////////////
//		Synchronizatiion of 2 swipers
//////////////////
mySwiper1.on('slideChange', function () {
	mySwiper2.slideTo(mySwiper1.realIndex, 1000, false);  //(index, speed(ms), runCallbacks)
});
mySwiper2.on('slideChange', function () {
	mySwiper1.slideTo(mySwiper2.realIndex, 1000, false);  //(index, speed(ms), runCallbacks)
});
 
 ///////////////////
//		Emergency stop：Space bar
//////////////////
document.onkeydown = function keydown() {
	if(event.keyCode == 32){	// Spacekey
		console.log(event.keyCode);
		location.href = 'file:titleimage/emergency.png'
	}
	else if(event.keyCode == 81){	// Q key
		console.log(event.keyCode);
		location.href = 'file:titleimage/final.png'
	}	
};


