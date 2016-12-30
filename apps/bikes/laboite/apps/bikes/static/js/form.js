(function($) {
    $(function() {
        // Add an hidden form field to store station name
        var $station = $('<input type="hidden" name="station" />').appendTo($('#appbikes_form'));

        // Provider has changed, reset autocomplete value
        $('#id_provider').change(function() {
            $('#id_id_station').val('').trigger('change');
        })

        // Id selected in autocomplete, we store station name in case of invalid form submission to reinit choices on page reload
        $('#id_id_station').on('select2:select', function(event) {
            $station.val(event.params.data.text);
        });
    });
})(jQuery);
