$(function(){
	// Top scroll
	$().UItoTop();

	// Main Navigation
	$('.muon').muon();

	// jQuery Tipsy
	$('.tooltip, .loading').tipsy({gravity:'s', fade:true}); // Tooltip Gravity Orientation: n | w | e | s
	$('.tooltip-wide').tipsy({gravity:'e', fade:true}); // Tooltip Gravity Orientation: n | w | e | s

	// Auto highlight mandatory inputs
	$('<span> *</span>').appendTo('.mandatory');

	// Check all checkboxes
	$('.check-all').click(
		function(){
			$(this).parents('form').find('input:checkbox').attr('checked', $(this).is(':checked'));
		}
	)

	// Notifications
	$('.notification-details').hide(); // Hide notification details
	$('.show-notification-details').click( //On click toggle notification details
		function () {
			$(this).next('.notification-details').slideToggle();
			return false;
		}
	);
	$('.close-notification').click( // On click slide up notification
		function () {
			$(this).parent().fadeTo(350, 0, function () {$(this).slideUp(600);});
			return false;
		}
	);

	// Content box tabs and sidetabs
	$('.tab, .sidetab').hide(); // Hide the content divs
	$('.default-tab, .default-sidetab').show(); // Show the div with class 'default-tab'
	$('.tab-switch a.default-tab, .sidetab-switch a.default-sidetab').addClass('current'); // Set the class of the default tab link to 'current'

	// Note: Tab ID have to be 'tabN', where N is number, or you would have to change regular expression to get hash working. Same applies for sidetabs.
	// 		 For more info about regular expressions please visit www.regular-expressions.info

	if(window.location.hash && window.location.hash.match(/^#tab\d+$/)) { // Check for tab Hash ID, if exist opens corresponding tab
		var tabID = window.location.hash; // Set variable tabID to the value of URL Hash

		$('.tab-switch a[href='+tabID+']').addClass('current').parent().siblings().find('a').removeClass('current'); // Find corresponding link and set is as current
		$('div'+tabID).parent().find('.tab').hide(); // Hide all content divs
		$('div'+tabID).show(); // Show the content div with the id equal to the id of URL Hash
		$('div'+tabID).find('.visualize').trigger('visualizeRefresh');; // Refresh jQuery Visualize
		$('.fullcalendar').fullCalendar('render'); // Refresh jQuery FullCalendar

	} else if (window.location.hash && window.location.hash.match(/^#sidetab\d+$/)) { // Check for sidetab Hash ID, if exist opens corresponding sidetab
		var sidetabID = window.location.hash;// Set variable sidetabID to the value of URL Hash

		$('.sidetab-switch a[href='+sidetabID+']').addClass('current'); // Find corresponding link and set is as current
		$('div'+sidetabID).parent().find('.sidetab').hide(); // Hide all content divs
		$('div'+sidetabID).show(); // Show the content div with the id equal to the id of URL Hash
		$('div'+sidetabID).find('.visualize').trigger('visualizeRefresh'); // Refresh jQuery Visualize
		$('.fullcalendar').fullCalendar('render'); // Refresh jQuery FullCalendar
	}

	$('.tab-switch a').click(
		function() {
			var tab = $(this).attr('href'); // Set variable 'tab' to the value of href of clicked tab
			$(this).parent().siblings().find('a').removeClass('current'); // Remove 'current' class from all tabs
			$(this).addClass('current'); // Add class 'current' to clicked tab
			$(tab).siblings('.tab').hide(); // Hide all content divs
			$(tab).show(); // Show the content div with the id equal to the id of clicked tab
			$(tab).find('.visualize').trigger('visualizeRefresh'); // Refresh jQuery Visualize
			$('.fullcalendar').fullCalendar('render'); // Refresh jQuery FullCalendar
			return false;
		}
	);

	$('.sidetab-switch a').click(
		function() {
			var sidetab = $(this).attr('href'); // Set variable 'sidetab' to the value of href of clicked sidetab
			$(this).parent().siblings().find('a').removeClass('current'); // Remove 'current' class from all sidetabs
			$(this).addClass('current'); // Add class 'current' to clicked sidetab
			$(sidetab).siblings('.sidetab').hide(); // Hide all content divs
			$(sidetab).show(); // Show the content div with the id equal to the id of clicked tab
			$(sidetab).find('.visualize').trigger('visualizeRefresh'); // Refresh jQuery Visualize
			$('.fullcalendar').fullCalendar('render'); // Refresh jQuery FullCalendar
			return false;
		}
	);

	// Content Header Options
	var optWidth = $('.options-switch').width();
	var btnWidth = $('.toggle-options-switch').width();
	$('.options-switch').hide().css({ 'margin-left':-(optWidth-btnWidth)/2 });
	$('.toggle-options-switch').click(
		function () {
			$(this).parent().parent().parent().siblings().find('.toggle-options-switch').removeClass('active').next().slideUp(); // Hide all menus expect the one clicked
			$(this).toggleClass('active').next().slideToggle(); // Toggle clicked menu
			$(document).click(function() { // Hide menu when clicked outside of it
				$('.options-switch').slideUp();
				$('.toggle-options-switch').removeClass('active')
			});
			return false;
		}
	);

	// Image actions
	$('.image-frame').hover( // On hover toggle image action menu
		function() {
			var imgHeight = $(this).find('img').height(); // Get image height
			$(this).find('.image-actions').css({ 'height':imgHeight-12 }).animate({width:'toggle'},250); // Resize image actions to image heigh - padding and slide it
		}
	);

	// Accordions
	$('.accordion li div').hide(); // Hide all content
	$('.accordion li:first-child div').show(); // Show first accordion content by default
	$('.accordion .accordion-switch').click( // On click hide all accordion content and open clicked one
		function() {
			$(this).parent().siblings().find('div').slideUp();
			$(this).next().slideToggle();
			return false;
		}
	);

});
