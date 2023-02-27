;(function(){
  const offcanvas = new bootstrap.Offcanvas(document.getElementById("offcanvas"));

  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "offcanvas") {
        offcanvas.show();
    }
  });

  htmx.on("htmx:beforeSwap", (e) => {
      // Hides dialog after form is submitted
      if (e.detail.target.id == "offcanvas" && !e.detail.xhr.response) {
        offcanvas.hide();
        e.detail.shouldSwap = false;
      }
    });
})()
