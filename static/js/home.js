document.addEventListener('DOMContentLoaded', function() {
    var locationSelect = document.getElementById('locationSelect');
    var changeCountryLink = document.getElementById('changeCountryLink');

    locationSelect.addEventListener('change', function() {
        var selectedOption = locationSelect.options[locationSelect.selectedIndex];
        var optionValue = selectedOption.value;

        // Redirect to the selected URL
        window.location.href = optionValue;
    });

    changeCountryLink.addEventListener('click', function(event) {
        event.preventDefault();
        // Handle change country link click event if needed
    });
});
