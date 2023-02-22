const chatSocket = (window.location.protocol != "https:") ?
  new WebSocket(
    "ws://" + window.location.host + "/ws/chat/" + room_id
  ) :
  new WebSocket(
    "wss://" + window.location.host + "/ws/chat/" + room_id
  );

/**
 * A function for finding the message element, and scroll to the bottom of it.
 */
function scrollToBottom() {
  let objDiv = document.getElementById("chat-messages");
  objDiv.scrollTop = objDiv.scrollHeight;
}

chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);

  if (data.message) {
    var tag = '';
    if (data.me) {
      tag += ('<div class="chat"><div><img src="/static/assets/pfp/' + me_id +
        '.jpeg" class="chat-profile-pic-right" alt="profile picture"></div><div ' +
        '<div class="message-me"><div class="message-text-right">' + data.message +
        '</div><br><div class="message-date-right">' + data.date_time + '</div></div></div>');
    } else {
      tag += ('<div class="chat"><div><img src="/static/assets/pfp/' + other_user_id +
        '.jpeg" class="chat-profile-pic-left" alt="profile picture"></div><div ' +
        '<div class="message-me"><div class="message-text-left">' + data.message +
        '</div><br><div class="message-date-left">' + data.date_time + '</div></div></div>');
    }
    document.querySelector("#chat-messages").innerHTML += tag;
    scrollToBottom();
  }
  scrollToBottom();
};


document.querySelector("#chat-message-input").focus();
document.querySelector("#chat-message-input").onkeyup = function(e) {
  if (e.keyCode === 13) { // "Enter"
    document.querySelector("#chat-message-submit").click();
  }
};

document.querySelector("#chat-message-submit").onclick = function(e) {
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
