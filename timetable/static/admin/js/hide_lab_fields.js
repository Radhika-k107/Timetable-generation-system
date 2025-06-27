document.addEventListener("DOMContentLoaded", function() {
    function toggleLabFields() {
        var isLabCheckbox = document.querySelector("#id_is_lab");
        var labField = document.querySelector(".form-row.field-lab");
        var practicalHoursField = document.querySelector(".form-row.field-practical_hours");
        var batchField = document.querySelector(".form-row.field-batches");

        if (isLabCheckbox.checked) {
            labField.style.display = "block";
            practicalHoursField.style.display = "block";
            batchField.style.display = "block";
        } else {
            labField.style.display = "none";
            practicalHoursField.style.display = "none";
            batchField.style.display = "none";
        }
    }

    var isLabCheckbox = document.querySelector("#id_is_lab");
    if (isLabCheckbox) {
        isLabCheckbox.addEventListener("change", toggleLabFields);
        toggleLabFields();  // Initial check
    }
});