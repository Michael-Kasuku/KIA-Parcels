function cancelForm() {
    var dashboardUrl = document.getElementById('send_parcel_form').getAttribute('dashboard-url');
    if (confirm("Are you sure you want to cancel? Any unsaved data will be lost.")) {
        window.location.href = dashboardUrl;
    }
}

function clearForm() {
    if (confirm("Are you sure you want to clear the form? Any unsaved data will be lost.")) {
        document.getElementById('send_parcel_form').reset();
    }
}
