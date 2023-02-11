// Add click listeners
$(".tablinks").each(function() {
  $(this).on("click", function (event) {
    openTab(event.currentTarget.id.slice(0,-4));
  });
});

// Open a tab
function openTab(content) {
  // Get all elements with class="tabcontent" and hide them
  $(".tabcontent").each(function() {
    $(this).hide();
  });

  // Get all elements with class="tablinks" and remove the class "active"
  $(".tablinks").each(function() {
    $(this).removeClass("active");
  });

  // Show the current tab, and add an "active" class to the link that opened the tab
  $("#" + content).show();
  $("#" + content + "_tab").addClass("active");
}
  
// Get the active tab from URL and open it (if there is anything)
var anchorHash = location.href;
if (anchorHash.lastIndexOf('#') != -1) {
  // Get the id from the end of the URL
  anchorHash = anchorHash.slice(anchorHash.lastIndexOf('#') + 1);
  $("#" + anchorHash + "_tab").click();
} else {
  // Default tab
  $("#details_tab").click();
}

//Add the listener to every select.
$(".select").each(function() {
  // If default value is changed.
  $(this).on("change", function () {
    // Get the button id
    var button_id = "#accept-" + $(this)[0].id.split("-")[1];
    // and enable it.
    $(button_id).prop("disabled", false);
  });
});

document.addEventListener("DOMContentLoaded", function(event) { 
  var scrollpos = localStorage.getItem('scrollpos');
  if (scrollpos) {
    window.scrollTo(0, scrollpos);
  };
});

window.onbeforeunload = function(e) {
  localStorage.setItem('scrollpos', window.scrollY);
};
