// Strange instruction but working!
if (window.jQuery) {

    // Hide alerts instead of dismiss them
    function hideAlertsInsteadOfRemove() {
        var $alert = $('.alert');

        $alert.find('.close').click(function() {
            $('.alert').slideUp();
        });
    }

    // Set a Notification (success, info, warning, danger)
    function setNotification(title, message, type) {
        var $notif = $('.notif');

        $notif.removeClass('alert-danger');
        $notif.removeClass('alert-info');
        $notif.removeClass('alert-warning');
        $notif.removeClass('alert-success');

        var classname = 'alert-' + type;

        $notif.addClass('alert-' + type);

        $notif.show();
        $notif.find('strong').text(title);
        $notif.find('span').text(message);
    }
    
    hideAlertsInsteadOfRemove();
}