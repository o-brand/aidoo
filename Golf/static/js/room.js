const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + room_id
);

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  if (data.message) {
    var tag = "<div "
    if (data.me) {
      tag += "class='message-me text-end'";
    }
    else {
      tag += "class='message-other'";
    }
    tag += ("><div class='message-username'>" + data.username + "</div><div class='message-text'>" + data.message + "</div></div>");
    document.querySelector("#chat-messages").innerHTML += tag;
  }
};

document.querySelector("#chat-message-input").focus();
document.querySelector("#chat-message-input").onkeyup = function (e) {
  if (e.keyCode === 13) { // "Enter"
    document.querySelector("#chat-message-submit").click();
  }
};

document.querySelector("#chat-message-submit").onclick = function (e) {
  e.preventDefault();

  const messageInputDom = document.querySelector("#chat-message-input");
  const message = messageInputDom.value;

  chatSocket.send(JSON.stringify({
      "message": message,
      "username": username,
  }));

  messageInputDom.value = "";

  return false;
};
