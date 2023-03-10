;(function(){
  const offcanvas = new bootstrap.Offcanvas(document.getElementById("offcanvas"));

  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "offcanvas") {
        offcanvas.show();
    }
  });
})()
