var personal = {
    list: function () {
        $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search'
                },
                dataSrc: ""
            },
            columns: [
                {"data": "id"},
                {"data": "user.names"},
                {"data": "user.dni"},
                {"data": "mobile"},
                {"data": "citybirth"},
                {"data": "typeblood"},
                {"data": "grade"},
                {"data": "birthdate"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    personal.list();

    $('#data').addClass('table-sm');
})
