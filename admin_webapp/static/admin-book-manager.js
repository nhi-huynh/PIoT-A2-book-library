// vim: set et sw=4 ts=4 sts=4:

$('#open-book-form').on('click', function() {
    open_book_form(false);
});

$('#book-submit').on('click', function(e) {
    e.preventDefault();
    save_book();
});

$('#book-delete').on('click', function(e) {
    e.preventDefault();
    delete_book();
});

$('body').on('click', '#book-table tbody tr', function() {
    var tr = $(this).closest('tr');

    var data = {
        isbn: tr.children('td:eq(0)').html(),
        title: tr.children('td:eq(1)').html(),
        author: tr.children('td:eq(2)').html(),
        year: tr.children('td:eq(3)').html()
    };

    open_book_form(data);
});

$('#form-close').on('click', close_book_form);

function open_book_form(data) {
    clear_book_form();
    var frm = $('#book-form');
    $('#book-msg').empty();

    if (data) {
        frm.find('#isbn-label').html('ISBN: ' + data.isbn);
        frm.find('[name=isbn]').val(data.isbn);
        frm.find('[name=title]').val(data.title);
        frm.find('[name=author]').val(data.author);
        frm.find('[name=yearPublished]').val(data.year);
        $('#book-delete').show();
    } else {
        frm.find('#isbn-label').html('ISBN: New');
        frm.find('[name=isbn]').val('new');
        $('#book-delete').hide();
    }

    $('#page-shadow').show();
    $('.book-form-container').css('display', 'flex');

    $(document).on('keyup.esc_close', function(e) {
        if (e.key == 'Escape') {
            close_book_form();
            $(document).unbind('keyup.esc_close');
        }
    });
}

function save_book() {
    var data = $('#book-form').serialize();
    var isbn = $('#book-form').find('[name=isbn]').val();

    if (isbn == 'new') {
        $.post('/api/book', data, save_action);
        return true;
    }

    $.ajax({
        url: '/api/book/' + isbn,
        type: 'PUT',
        data: data,
        success: save_action
    });
    // $.put('/api/book/' + isbn, data, save_action);
}

function save_action(data, status) {
    var msg = $('#book-msg');
    msg.empty();

    if (status != 'success') {
        msg.html('Failed to save book (bad request)');
        return false;
    }

    if (data.ISBN) {
        msg.html('Saved');
        setTimeout(close_book_form, 600);
        reload_books();
        return false;
    } else {
        msg.html('Failed to save book');
    }
}

function delete_book() {
    var isbn = $('#book-form').find('[name=isbn]').val();

    if (isbn == 'new') return false;

    $.ajax({
        url: '/api/book/' + isbn,
        type: 'DELETE',
        success: delete_action
    });
}

function delete_action(data, status) {
    var msg = $('#book-msg');
    msg.empty();

    if (status != 'success') {
        msg.html('Failed to delete book (bad request)');
        return false;
    }

    msg.html('Book deleted');

    setTimeout(close_book_form, 600);
    reload_books();
}

function close_book_form() {
    console.log('closing');
    $('#page-shadow').hide();
    $('.book-form-container').hide();
}

function clear_book_form() {
    $('#book-form input:not([type=submit])').val('');
}


function reload_books() {
    var msg = $('#msg-book-html');
    msg.empty();

    $.get('/api/book', function(data, status) {
        if (status != 'success') {
            msg_text = 'An error occurred while loading the book table (invalid request)';
            msg.html('<span class="error">' + msg_text + '</span>');
            return false;
        }

        try {
            data = JSON.parse(data);
        } catch (err) {
            msg_text = 'An error occurred while loading the book table (invalid response)';
            msg.html('<span class="error">' + msg_text + '</span>');
        }

        var fields = [
            'ISBN',
            'Title',
            'Author',
            'YearPublished'
        ];

        var tbody = $('#book-table tbody');
        tbody.empty();

        $.each(data, function(i,e) {
            var tr = '<tr data-isbn="' + e['ISBN'] + '">';

            $.each(fields, function(fi, fe) {
                tr += '<td>' + e[fe] + '</td>';
            });

            tr += '</tr>';

            tbody.append(tr);
        });
    });
}

reload_books();
