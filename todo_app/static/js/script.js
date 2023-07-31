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
    });

}