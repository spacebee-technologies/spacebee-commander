showLatestImage()
function showLatestImage() {
    var buttons = document.querySelectorAll('.nav-link');
    var latestButton = buttons[0]; // Get the first button initially

    // Find the button with the latest timestamp
    buttons.forEach(function(button) {
        if (button.getAttribute('data-image') > latestButton.getAttribute('data-image')) {
            latestButton = button;
        }
    });

    // Show the image associated with the latest timestamp
    showImage(latestButton);
}
function showImage(button) {
    var timestamp = button.getAttribute('data-image');
    var imgElement = document.getElementById('selected-image');
    var buttons = document.querySelectorAll('.nav-link');
    var titleImageElement = document.getElementById('image-title');

    timestampText = button.innerText;
    

    imgElement.src = serverUrl+'/images/image_' + timestamp+'.jpeg';
    titleImageElement.innerText = timestampText;
    // Remove active class from all buttons
    buttons.forEach(function(btn) {
        btn.classList.remove('active');
    });

    // Add active class to the clicked button
    button.classList.add('active');
}

function send_TC(btn) {
    var idTC = btn.getAttribute('id');
    var dataToSend = {
      idTC: idTC
    };

    // Send AJAX request to the server
    $.ajax({
      url: '/send_TC', // URL of the server endpoint
      type: 'POST',
      data: JSON.stringify(dataToSend), // Convert data to JSON string
      contentType: 'application/json', // Set content type to JSON
      success: function(response){
        alert(JSON.stringify(response)); // Display the result from the server
      },
      error: function(error){
        console.log(error); // Log any errors to the console
      }
    });
  }