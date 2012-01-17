$(function(){
	
	// For demo only
	$('.extension, .emoticon').tipsy({gravity:'s', title: 'class'}); // Show extensions classes
	
	// Top scroll
	$().UItoTop();
	
	// Main Navigation
	$('.muon').muon();
	
	// jQuery Tipsy
	$('.tooltip, .loading').tipsy({gravity:'s', fade:true}); // Tooltip Gravity Orientation: n | w | e | s
	$('.tooltip-wide').tipsy({gravity:'e', fade:true}); // Tooltip Gravity Orientation: n | w | e | s
	
	// jQuery dataTables
	$('.datatable').dataTable({ 'sPaginationType':'full_numbers' });
	
	// jQuery jWYSIWYG Editor
	$('.wysiwyg').wysiwyg({ iFrameClass:'wysiwyg-iframe' });

	// jQuery Custom File Input
	$('.fileupload').customFileInput();

	// jQuery DateInput
	$('.datepicker').after('<span class="datepicker-icon">&nbsp;</span>').datepick({ pickerClass: 'jq-datepicker' });
	
	// jQuery nyroModal
	$('.modal').nyroModal();

	// jQuery Snippet (Syntax Highlighter)
	$('pre.htmlCode').snippet('html',{style:'bright'});
	$('pre.jsCode').snippet('javascript',{style:'bright'});
	$('pre.cssCode').snippet('css',{style:'bright'});
	$('pre.phpCode').snippet('php',{style:'bright'});

	// IE7 doesn't support :disabled
	$('.ie7').find(':disabled').addClass('disabled');
	
	// IE7 notification fix
	$('.ie7').find('.muon .small-notification').wrapInner('<b />');
	
	// Auto highlight mandatory inputs
	$('<span> *</span>').appendTo('.mandatory');
	
	// Check all checkboxes
	$('.check-all').click(
		function(){
			$(this).parents('form').find('input:checkbox').attr('checked', $(this).is(':checked'));
		}
	)
	
	// Minimize Content Article
	$('.minimizer header').each(function() {
		var h2Width = $(this).find('h2').width();
		$(this).append('<a href="#" class="content-box-minimizer" title="Toggle Content Block">Toggle</a>'); // Add minimizer iocn 
		$(this).find('.content-box-minimizer').css({'display':'block', 'left':h2Width+35}).parent().find('h2').css({'padding-right':'90px'}); // Change style for minimizer
	});
	$('.minimizer .content-box-minimizer').click( // On click toggle content window and add class 'toggled'
		function () {
			$(this).toggleClass('toggled');
			$(this).parent().find('nav').toggle();
			$(this).parent().parent().toggleClass('toggled').find('section, footer').toggle();
			return false;
		}
	);
	
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
	
	// Comments
	$('.post').find('ul').addClass('comments-collapsed').children('li.comment').hide();
	$('.post .view-comments a, .post .comments-collapsed textarea').click(
		function () {
			var current = $(this).parents('.post');
			$(current).find('ul.comments-collapsed').removeClass('comments-collapsed').addClass('comments-expanded');
			$(current).find('ul.comments-expanded').find('.comment').slideDown(function() {
				$(current).find('ul.comments-expanded').find('.view-comments').fadeOut().next('li').css('border-radius', '3px 3px 0 0'); 
			});
			return false;
		}
	);
	$('.post .comments-collapsed textarea').click(
		function () {
			if( $(this).text() == 'Write comment…' ) {
				$(this).text('');
			}
		}
	);

	// Targeting Opera 11 and older Opera browsers
	if (window.opera && window.opera.version() < 12) {
		document.documentElement.className += ' opera11';
	};

	// jQuery Data Visualize
	$('table.data').each(function() {
		var chartWidth = Math.floor($(this).parent().width()*0.90); // Set chart width to 90% of its parent
		var chartType = ''; // Set chart type
			
		if ($(this).attr('data-chart')) { // If exists chart-chart attribute
			chartType = $(this).attr('data-chart'); // Get chart type from data-chart attribute
		} else {
			chartType = 'area'; // If data-chart attribute is not set, use 'area' type as default. Options: 'bar', 'area', 'pie', 'line'
		}
		
		if(chartType == 'line' || chartType == 'pie') {
			$(this).hide().visualize({
				type: chartType,
				width: chartWidth,
				height: '240px',
				colors: ['#f29785', '#aff285', '#85d2f2', '#f2f085', '#b3afaf'],
				lineDots: 'double',
				interaction: true,
				multiHover: 5,
				tooltip: true,
				tooltiphtml: function(data) {
					var html ='';
					for(var i=0; i<data.point.length; i++){
						html += '<p class="chart_tooltip"><strong>'+data.point[i].value+'</strong> '+data.point[i].yLabels[0]+'</p>';
					}	
					return html;
				}
			});
		} else {
			$(this).hide().visualize({
				type: chartType,
				width: chartWidth,
				height: '240px',
				colors: ['#f29785', '#aff285', '#85d2f2', '#f2f085', '#b3afaf']
			});
		}
	});
	//$('.ie8').find('.visualize').trigger('visualizeRedraw');

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

	// Table actions
	var optWidth = $('.table-switch').outerWidth();
	var btnWidth = $('.toggle-table-switch').outerWidth();
	$('.table-switch').hide().css({ 'margin-left':-(optWidth-btnWidth)/2 });
	$('.ie7 .table-switch').css({ 'margin-left':-btnWidth+3 }); // Don't ask why...
	
	$('.toggle-table-switch').click(
		function () {
			$(this).parent().parent().siblings().find('.toggle-table-switch').removeClass('active').next().slideUp(); // Hide all menus expect the one clicked
			$(this).toggleClass('active').next().slideToggle(); // Toggle clicked menu
			$(document).click(function() { // Hide menu when clicked outside of it
				$('.table-switch').slideUp();
				$('.toggle-table-switch').removeClass('active')
			});
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
	
	// Tickets
	$('.tickets .ticket-details').hide(); // Hide all ticket details
	$('.tickets .ticket-open-details').click( // On click hide all ticket details content and open clicked one
		function() {
			//$('.tickets .ticket-details').slideUp()
			$(this).parent().parent().parent().parent().siblings().find('.ticket-details').slideUp(); // Hide all ticket details expect the one clicked
			$(this).parent().parent().parent().parent().find('.ticket-details').slideToggle();
			return false;
		}
	);
	
	// Wizard
	$('.wizard-content').hide(); // Hide all steps
	$('.wizard-content:first').show(); // Show default step
	$('.wizard-steps li:first-child').addClass('wizard-step-done').find('a').addClass('current');
	$('.wizard-steps a').click(
		function() { 
			var step = $(this).attr('href'); // Set variable 'step' to the value of href of clicked wizard step
			$('.wizard-steps a').removeClass('current');
			$(this).addClass('current').parent('li').addClass('wizard-step-done');
			$(this).parent('li').prevAll().addClass('wizard-step-done'); // Mark all prev steps as done
			$(this).parent('li').nextAll().removeClass('wizard-step-done'); // Mark all next steps as undone
			$(step).siblings('.wizard-content').hide(); // Hide all content divs
			$(step).fadeIn(); // Show the content div with the id equal to the id of clicked step
			return false;
		}
	);
	$('.wizard-next').click(
		function() { 
			var step = $(this).attr('href'); // Set variable 'step' to the value of href of clicked wizard step
			$('.wizard-steps a').removeClass('current');
			$('.wizard-steps a[href="'+step+'"]').addClass('current').parent('li').addClass('wizard-step-done');
			$('.wizard-steps a[href="'+step+'"]').parent('li').prevAll().addClass('wizard-step-done'); // Mark all prev steps as done
			$('.wizard-steps a[href="'+step+'"]').parent('li').nextAll().removeClass('wizard-step-done'); // Mark all next steps as undone
			$(step).siblings('.wizard-content').hide(); // Hide all content divs
			$(step).fadeIn(); // Show the content div with the id equal to the id of clicked step
			return false;
		}
	);
	
	// Progress bar animation
	$('.progress-bar').each(function() {
		var progress = $(this).children().width();
		$(this).children().css({ 'width':0 }).animate({width:progress},3000);
	});
	
	//jQuery Full Calendar
	var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();
	
	$('.fullcalendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,basicWeek,basicDay'
		},
		editable: true,
		events: [
			{
				title: 'All Day Event',
				start: new Date(y, m, 1)
			},
			{
				title: 'Long Event',
				start: new Date(y, m, d-5),
				end: new Date(y, m, d-2)
			},
			{
				id: 999,
				title: 'Repeating Event',
				start: new Date(y, m, d-3, 16, 0),
				allDay: false
			},
			{
				id: 999,
				title: 'Repeating Event',
				start: new Date(y, m, d+4, 16, 0),
				allDay: false
			},
			{
				title: 'Meeting',
				start: new Date(y, m, d, 10, 30),
				allDay: false
			},
			{
				title: 'Lunch',
				start: new Date(y, m, d, 12, 0),
				end: new Date(y, m, d, 14, 0),
				allDay: false
			},
			{
				title: 'Birthday Party',
				start: new Date(y, m, d+1, 19, 0),
				end: new Date(y, m, d+1, 22, 30),
				allDay: false
			},
			{
				title: 'Click for Parallaq',
				start: new Date(y, m, 28),
				end: new Date(y, m, 29),
				url: 'http://www.parallaq.com/'
			}
		]
	});

});