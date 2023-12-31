function statusCheckBoxChange(todoItemId) {
    var checkBoxId = "#status_" + todoItemId;
    var todoItemStatus = $(checkBoxId).is(':checked')

    $.ajax({
        url: "/complete_item",
        type: 'POST',
        data: {
            itemId: todoItemId,
            status: todoItemStatus
        }
    })
    .always(function() {
        window.location.href="/"
    });

}

function deleteItem(todoItemId) {
    $.ajax({
        url: "/deleteItem",
        type: 'POST',
        data: {
            itemId: todoItemId
        }
    })
    .always(function() {
        window.location.href="/"
    });
}

