$(".form-buy").each(function() {
    $(this).on("click", function (event) {
      console.log("Something happens")
      location.reload()
    });
});
