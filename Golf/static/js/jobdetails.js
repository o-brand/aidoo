const jobSocket = (window.location.protocol != "https:") ?
  new WebSocket(
    "ws://" + window.location.host + "/ws/job/" + job_id
  ) :
  new WebSocket(
    "wss://" + window.location.host + "/ws/job/" + job_id
  );

jobSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);

  if (data.content) {
    var tag = '<div class="card details-card mb-2"><div class="card-body">' +
      '<div class="d-flex justify-content-start card-subtitle mb-1 text-muted">' +
      '<a href="/profile/' + data.commenter_id + '"><img src="/static/assets/pfp/' +
      data.commenter_id + '.jpeg"></a><h5><a href="/profile/' + data.commenter_id +
      '">' + data.commenter;
    if (data.commenter_id == poster_id) {
      tag += ' (Poster)';
    }
    tag += '</a></h5></div><p>' + data.content + '</p><p>' + data.date_time +
      '</p></div></div>';
    document.querySelector("#comments").innerHTML += tag;
  }
};


document.querySelector("#job-message-input").focus();
$("#job-message-input").keydown(function (event) {
  event = (event) ? event : ((window.event) ? window.event : "");
  var keyCode = event.keyCode ? event.keyCode : (event.which ? event.which : event.charCode);
  var altKey = event.ctrlKey || event.metaKey;
  if (keyCode === 13 && altKey) { //ctrl+enter
    var newDope = $(this).val() + "\n";// Get textarea data for newline
    $(this).val(newDope);
  } else if (keyCode === 13) { // "Enter"
    event.preventDefault();
    document.querySelector("#job-message-submit").click();
  }
});


document.querySelector("#job-message-submit").onclick = function(e) {
  e.preventDefault();

  const messageInputDom = document.querySelector("#job-message-input");
  const message = messageInputDom.value;

  jobSocket.send(JSON.stringify({
    "content": message,
    "commenter": username,
    "commenter_id": me_id,
  }));
  messageInputDom.value = "";
  return false;
};
