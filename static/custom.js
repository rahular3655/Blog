document.addEventListener('DOMContentLoaded', function() {
    var emailField = document.querySelector('.active-email-field');
    if (emailField) {
        var tickmarkSpan = document.createElement('span');
        tickmarkSpan.innerHTML = '&#10003;';  // Unicode character for tickmark
        emailField.parentNode.appendChild(tickmarkSpan);
    }
});
