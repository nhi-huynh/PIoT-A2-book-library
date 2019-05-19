// vim: set et sw=4 ts=4 sts=4:

function show_loading(el) {
    /*
     * Shows the "Loading . . ." message in el
     * Returns intervalID : int
     * Will keep displaying until the caller manually clears the interval
     */

    var x = 1;

    el.html('Loading .');

    return setInterval( function() {
        el.html('Loading' + ' .'.repeat(x + 1));
        x = (x + 1) % 3;
    }, 500);
}

$('#login-form').on('submit', function(e) {
    /*
     * Submits the form and attempts to login
     * If the login fails for any reason, a
     * relevant message is displayed
     * if successful, redirect to /admin
     */
    e.preventDefault();

    // Disable Login button while waiting for response
    $('#login-action').prop('disabled', true);

    var data = {
        ajax: true,
        user: $('#username').val(),
        pass: $('#password').val()
    };

    var msg = $('#login-form .msg');

    // Show "Loading ..."
    var repeat = show_loading(msg);

    // Post the info
    $.post('/login', data, function(data, status) {

        // Enable the Login button again and clear the interval
        $('#login-action').prop('disabled', false);
        clearInterval(repeat);

        // Clear any previous messages
        msg.empty();
        
        if (status != 'success') {
            // Request failed
            msg_text = 'A problem occurred when trying to log in, please try again';
            msg_text = '<span class="error">' + msg_text + '</span>';

            msg.html(msg_text);
            return false;
        }

        // Attempt to decode json response
        try {
            data = JSON.parse(data);
        } catch (err) {
            msg_text = 'A problem occurred when trying to log in, please try again';
            msg_text = '<span class="error">' + msg_text + '</span>';

            msg.html(msg_text);
            return false;
        }

        if (!data.auth_success) {
            // Login failed
            msg.html('Invalid credentials, please try again');
            return false;
        }

        // Login successful, redirect
        document.location = '/admin';
    });
});
