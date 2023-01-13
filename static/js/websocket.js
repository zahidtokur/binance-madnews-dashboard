let socket = new WebSocket("wss://www.madnews.io/ws");

socket.onopen = function (e) {
  socket.send("ping");
};

socket.onmessage = function (event) {
    try {
        data = JSON.parse(event.data);
        console.log(data);
        if (data.link) {
          createTweetToast(data);
        } else {
          createPostToast(data);
        }
    } catch (error) {}
};

socket.onclose = function (event) {
  console.log("Socket connection closed.");
};
