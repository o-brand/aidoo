;(function(){
  htmx.on("htmx:beforeSwap", (e) => {
    if (e.detail.target.id == "start-chat") {
      htmx.ajax('GET', '/chat/refresh-rooms', { target: '#rooms-list', swap:'outerHTML'})
    }
  });
})()
