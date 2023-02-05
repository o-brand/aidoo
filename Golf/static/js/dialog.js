;(function(){
  const modal = new bootstrap.Modal(document.getElementById("modal"));

  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "dialog") {
        modal.show();
    }
  });

  htmx.on("htmx:beforeSwap", (e) => {
      // Hides dialog after form is submitted
      if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        modal.hide();
        e.detail.shouldSwap = false;
      }
    });

  htmx.on("hidden.bs.modal", (e) => {
    // Clear form after modal is hidden
    document.getElementById("dialog").innerHTML = "";
  });
})()