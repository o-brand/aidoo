;(function(){

  htmx.on("htmx:beforeSwap", (e) => {
      // Hides dialog after form is submitted
      console.log(e)
      if (e.detail.target.id == "start-chat") {
          htmx.ajax('GET', '/chat/refresh-rooms', {target: '#rooms-list', swap:'outerHTML'})
      }
    });


})()
