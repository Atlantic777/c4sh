// frontend definitions

errorNotification = function(msg, title) {

	if (typeof(title) == "undefined" || !title)
		title = "Error";

	var id = 'notification_error_'+new Date().getTime();

	var html = '<div id="'+id+'" class="notification error"><h4>'+title+'</h4><p>'+msg+'</p></div>';

	$('section[role=main]').prepend(html);

	setTimeout(function() {
		$('#'+id).fadeOut();
	}, 3000);
};

successNotification = function(msg, title) {

	if (typeof(title) == "undefined" || !title)
		title = "Success";

	var id = 'notification_success_'+new Date().getTime();

	var html = '<div id="'+id+'" class="notification success"><h4>'+title+'</h4><p>'+msg+'</p></div>';

	$('section[role=main]').prepend(html);

	setTimeout(function() {
		$('#'+id).fadeOut();
	}, 3000);
};