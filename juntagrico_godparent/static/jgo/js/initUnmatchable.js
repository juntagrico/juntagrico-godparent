$(function(){
    $("#filter-table-godparents").DataTable({
        "paging": false,
        "info": false,
        "ordering": true,
        "search": {
            "regex": true,
            "smart": false
        },
        "language": {
            "search": search_field,
            searchBuilder: sb_lang
        },
    })
})
