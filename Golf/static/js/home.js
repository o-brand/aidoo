;(function(){
  const scrollButton = document.getElementById("btn-back-to-top");

  window.onscroll = function () {
    if (document.body.scrollTop > 20 ||
      document.documentElement.scrollTop > 20) {
      scrollButton.style.display = "block";
    } 
    else {
      scrollButton.style.display = "none";
    }
  };

  // Event listener for clicking, this scrolls back up to the top when triggered
  scrollButton.addEventListener("click", ()=>{
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  });
})()
