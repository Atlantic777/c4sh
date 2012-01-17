// jQuery Muon Dropdown Menu plugin

(function($) {

	$.muon = function(element, options) {

		// Plugin's default options, this is private property and is accessible only from inside the plugin
		var defaults = {

			speed: 500,  // Animation speed
			offset: 15,  // Animation offest in percentage, 15 = 15%
			navEffect: 'slide', // Main navigation animation, leave blank for simple show/hide effect, options:  slide, bounce
			subnavEffect: 'slide',  // Subnavigation animation, leave blank for simple show/hide effect, options: fade, slide
			fixHeight: false // Use highest subnavigation for all

		}

		// To avoid confusions, use "plugin" to reference the current instance of the object
		var plugin = this;

		// This will hold the merged default and user-provided options
		plugin.settings = {}

		var $element = $(element),	// Reference to the jQuery version of DOM element the plugin is attached to
			element = element;		// Reference to the actual DOM element

		// The "constructor" method that gets called when the object is created
		plugin.init = function() {

			// The plugin's final properties are the merged default and user-provided options (if any)
			plugin.settings = $.extend({}, defaults, options);
			
			// Add constructor's classes
			$element.addClass('muon_init').find('nav').closest('ul').addClass('muon_root');
			
			// Recalculate notifications
			$element.find('.small-notification').each(function() {
				var parenWidth = $(this).parent('li').width();
				$(this).css('marginLeft', parenWidth-28);
			});
			
			// Hide all subnavigations
			$element.find('nav nav').hide();
			
			// Stop propagation of events if clicked inside of navigation
			$($element).click(function(event){
				event.stopPropagation();
			});
			
			// Take care of navigation
			plugin.menu_handler();

		}
		
		plugin.menu_handler = function() {
			
			// Function to clear and set current item where A is current item and B is group of all items
			var classer = function(a, b) {
				$(b).removeClass('muon_current_item');
				$(a).addClass('muon_current_item');
			} 
			
			// Get all main navigation anchors (plugin takes only anchors followed with nav)
			var $anchors = $element.find('nav nav').prevAll('a');
			
			// Set main navigation container height
			var mainNavHeight = $element.height();
			
			// If main navigation anchor is clicked
			$anchors.click(function() {
				
				// Chceck if main navigation container is already open
				if($element.hasClass('muon_opened')) {
					
					if($(this).hasClass('muon_current_item')) { // If clicked current subnavigation, close the navigation
						plugin.hide_menu($anchors, mainNavHeight);
						
					}else if(!plugin.settings.fixHeight) { // Resize main navigation contaier if we don't use fixed height
						var nextNavHeight = $(this).nextAll('nav').outerHeight()+mainNavHeight;
						$element.animate({height:nextNavHeight},250);
						classer(this, $anchors);
						plugin.submenu_handler(this);
						
					}else{ // Switch class and show subnavigation
						classer(this, $anchors);
						plugin.submenu_handler(this);
						
					}

				}else{
					
					// Set subnavigation height variable
					var subNavHeight = 0;
					
					if(plugin.settings.fixHeight) { // Set highest subnavigation container height
						$anchors.nextAll('nav').each(function(){
							if(subNavHeight < $(this).outerHeight()) subNavHeight = $(this).outerHeight();
						});
						var subNavHeight = subNavHeight+mainNavHeight;
						
					}else{ // Set current subnavigation container height
						var subNavHeight = $(this).nextAll('nav').outerHeight()+mainNavHeight;
						
					}
					
					// Set animation offset height
					var offsetNavHeight = subNavHeight*(plugin.settings.offset*0.01+1);
					
					// Add .muon_opened class to main container
					$element.addClass('muon_opened');
					
					// Menu animation effects
					switch(plugin.settings.navEffect) {
						case 'slide':
							$element.animate({height:offsetNavHeight},plugin.settings.speed).animate({height:subNavHeight},plugin.settings.speed);

							break;
						case 'bounce':
							$element.animate({height:subNavHeight},plugin.settings.speed).animate({height:'-=25'},250).animate({height:'+=25'},185).animate({height:'-=15'},280).animate({height:'+=15'},215);

							break;
						default:
							$element.css({height:subNavHeight});

					}
					
					// Switch class
					classer(this, $anchors);
					
					// Hide notifications
					$element.find('.small-notification').fadeOut();
					
					// Take care of subnavigation effects
					plugin.submenu_handler(this);

				}
				return false;
			});
			
			// Hide navigation if clicked outside of it
			$(document).click(function() {
				if($element.hasClass('muon_opened')) {
					plugin.hide_menu($anchors, mainNavHeight);
				}
			});
		}
		
		plugin.submenu_handler = function(a) {
			
			$element.find('nav nav').hide();
			
			// Submenu animation effects
			switch(plugin.settings.subnavEffect) {
				case 'fade': // Fade in and out
					$(a).nextAll('nav').fadeToggle();

					break;
				case 'slide': // Slide from left to right
					var $target = $(a).nextAll('nav');
					var targetWidth = $target.width();
					$target.css({left:0, left:-targetWidth}).show();
					
					$target.animate({
					  left: parseInt($target.css('left'),10) == 0 ?
						-$target.outerWidth() :
						0
					});

					break;
				default: // Show and hide
					$(a).nextAll('nav').toggle();
			}
		}
		
		plugin.hide_menu = function($anchors, mainNavHeight) {
			
			var offsetNavHeight = $element.height()*(plugin.settings.offset*0.01+1);
			
			switch(plugin.settings.navEffect) {
				case 'slide':					
					$element.animate({height:offsetNavHeight}).animate({height:mainNavHeight},plugin.settings.speed, function () {
						$element.find('.small-notification').fadeIn(); // Show notifications
					});
					break;
				case 'bounce':
					$element.animate({height:mainNavHeight},plugin.settings.speed, function () {
						$element.find('.small-notification').fadeIn(); // Show notifications
					});

					break;
				default:
					$element.css({height:mainNavHeight}, function () {
						$element.find('.small-notification').fadeIn(); // Show notifications
					});
			}
			
			$anchors.removeClass('muon_current_item');
			$element.removeClass('muon_opened');
			$element.find('nav nav').hide();
		}

		// Call the "constructor" method
		plugin.init();

	}

	// Add the plugin to the jQuery.fn object
	$.fn.muon = function(options) {

		// Iterate through the DOM elements we are attaching the plugin to
		return this.each(function() {

			// If plugin has not already been attached to the element
			if (undefined == $(this).data('muon')) {

				// Create a new instance of the plugin and pass the DOM element and the user-provided options as arguments
				var plugin = new $.muon(this, options);

				// in the jQuery version of the element
				// store a reference to the plugin object
				// you can later access the plugin and its methods and properties like
				// element.data('muon').publicMethod(arg1, arg2, ... argn) or
				// element.data('muon').settings.propertyName
				$(this).data('muon', plugin);
			}
		});
	}

})(jQuery);