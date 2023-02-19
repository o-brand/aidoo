const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + room_id
);

/**
* A function for finding the message element, and scroll to the bottom of it.
*/
function scrollToBottom() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}

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
    tag += ("><div class='message-text'>" + data.message + 
      "</div><div class='message-date'>" + data.date_time + 
      "</div><div class='message-username'>");

    if (data.me) {
      tag += "Me";
    }
    else {
      tag += data.username;
    }
    tag += data.username +"</div></div>";
    document.querySelector("#chat-messages").innerHTML += tag;
  }
  scrollToBottom();
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

scrollToBottom();
