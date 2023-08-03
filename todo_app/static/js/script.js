function statusCheckBoxChange(todoItemId) {
    var checkBoxId = "#status_" + todoItemId;
    var todoItemStatus = $(checkBoxId).is(':checked')

    $.ajax({
        url: "/markComplete",
        type: 'POST',
        data: {
            itemId: todoItemId,
            status: todoItemStatus
        }
    })
    .always(function($response) {
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
    .always(function($response) {
        window.location.href="/"
    });
}

