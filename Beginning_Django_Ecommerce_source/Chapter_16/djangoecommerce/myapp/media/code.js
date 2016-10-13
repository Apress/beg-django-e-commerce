(function($) {
  $('#clickme').live('click', function() {
    $(this).append(' Click!');
  });
})(jQuery);
