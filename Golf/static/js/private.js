// Open a tab
function openTab(evt, content) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(content).style.display = "block";
    evt.currentTarget.className += " active";
  }
  
  // Get the active tab from URL and open it (if there is anything)
  var anchorHash = location.href;
  if (anchorHash.lastIndexOf('#') != -1) {
    // Get the id from the end of the URL
    anchorHash = anchorHash.substr(anchorHash.lastIndexOf('#') + 1);
    document.getElementById(anchorHash + "_tab").click();
  } else {
    // Default tab
    document.getElementById("details_tab").click();
  }
  
  // Get all the selects from the page
  let selects = document.getElementsByClassName("select");
  
  //Add the listener to every select.
  Array.prototype.forEach.call(selects, function(select) {
    // When user clicked on select element.
    select.addEventListener("click", () => {
      // If default value is changed.
      select.addEventListener("change", () => {
        // Get the button id
        var button_id = "accept-" + select.id.split("-")[1]
        // and enable it.
        document.getElementById(button_id).disabled = false;
      });
    });
  });
