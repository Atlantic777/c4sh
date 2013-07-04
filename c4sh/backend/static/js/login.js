$(function(){
	// jQuery Tipsy
	$('[rel=tooltip], .loading').tipsy({gravity:'s', fade:true}); // Tooltip Gravity Orientation: n | w | e | s
	
	// IE7 doesn't support :disabled
	$('.ie7').find(':disabled').addClass('disabled');
	
	// Auto highlight mandatory inputs
	$('<span> *</span>').appendTo('.mandatory');
	
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
	
	// Froms switch
	$('#regform, #regaction').hide(); // Hide registration form
	$('.regtoggle').click( //On click toggle registration
		function () {
			$('#logform, #logaction').slideToggle();
			$('#regform, #regaction').slideToggle();
			return false;
		}
	);
});