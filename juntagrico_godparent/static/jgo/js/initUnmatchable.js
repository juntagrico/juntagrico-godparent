$(function(){
    let data_table = create_data_table($("#filter-table-godparents"))
    add_filters(data_table)
    datatable_styling()
})


// TODO: move all of these to core juntagrico

// replaces table_column_search
function add_filters(data_table) {
    data_table.columns().every(function () {
        let tr = $(this.header())
        if (tr.is('.filter')) {
            let that = this

            let input = $("<input type='text' placeholder='' style='width: 100%;' class='form-control input-sm' />")
            input.on("click", function (e) {
                e.preventDefault()
                e.stopPropagation()
            })
            input.on("keyup change", function () {
                if (that.search() !== this.value) {
                    that.search(this.value, true, false).draw();
                }
            })
            tr.append(input)
        }
    })
}

function create_data_table(table) {
    return table.DataTable({
        "paging": false,
        "info": false,
        "search": {
            "regex": true,
            "smart": false
        },
        "drawCallback": function (settings) {
            // do not like this but it works so far till i get around to find the correct api call
            updateSendEmailButton(fetch_emails().length);
        },
        "language": {
            "search": search_field,
            searchBuilder: sb_lang
        },
        searchBuilder: get_sb_config(),
        dom : get_dom(),
    })
}

// TODO: replaces decorate_man_list_inputs and align_filter
 function datatable_styling() {
    // TODO: move this to a css file
    $(".dataTables_filter").css("text-align","right")
    $(".dataTables_filter label input")
        .addClass("form-control input-sm")
        .css("width","auto")
        .css("display","inline")
 }