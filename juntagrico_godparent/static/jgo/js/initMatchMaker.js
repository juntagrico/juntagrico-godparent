$(function(){
    // initialize based on checked boxes
    $('.possible-match input:checked').each(function() {
        update_remaining($(this))
    })

    // update on change
    $('.possible-match input').on('change', function() {
        update_remaining($(this))
    })
})

function update_remaining(input_element) {
    let [godparent, godchild] = input_element.attr('id').split('-').slice(1)
    let this_row = input_element.closest('tr')
    if(input_element.is(':checked')) {
        $('.godparent-' + godparent + ' .remaining-godchildren').each(function() {
            let td = $(this)
            let new_val = td.text()-1
            td.text(new_val)
            if (new_val === 0 && (td.parent().find('input')).is(':not(:checked)')) {
                td.parent().addClass('hide-godparent-' + godparent)
            }
        })
        $('.godchild-' + godchild).not(this_row).addClass('hide-godchild-' + godchild)
    } else {
        $('.godparent-' + godparent + ' .remaining-godchildren').each(function() {
            $(this).text(parseInt($(this).text())+1).parent().removeClass('hide-godparent-' + godparent)
        })
        $('.godchild-' + godchild).removeClass('hide-godchild-' + godchild)
    }
}