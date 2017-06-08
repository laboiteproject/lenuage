$('#id_asana_personal_access_token').change(function(e) {
    var $self = $(this),
        accessToken = $self.val(),
        $select = $('#id_asana_project_id');
    if (!accessToken) {
        return;
    }
    var $spinner = $('<i>').attr('id', 'spinner')
                           .css('marginLeft', '10px')
                           .addClass('fa fa-spinner fa-spin fa-fw');
    $select.closest('.form-group').find('.control-label').append($spinner);
    $.getJSON('../projects', {access_token: accessToken})
        .done(function(data) {
            $spinner.remove();
            $self.closest('.form-group').removeClass('has-error');
            $select.empty();
            if (!data.length) {
                return;
            }
            $.each(data, function (index, value) {
                $select.append($('<option>').val(value.id).text(value.name));
            });
            $select.removeAttr('disabled');
        })
        .fail(function() {
            $spinner.remove();
            $select.empty();
            $self.closest('.form-group').addClass('has-error');
            $select.attr('disabled', 'disabled');
        });
});
