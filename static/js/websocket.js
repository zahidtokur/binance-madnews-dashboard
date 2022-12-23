let socket = new WebSocket("wss://www.madnews.io/ws");

socket.onopen = function (e) {
  socket.send("ping");
};

socket.onmessage = function (event) {
    try {
        data = JSON.parse(event.data);
        console.log(data);
        if (data._id) {
          createPostToast(data);
        } else if (data.info.twitterId) {
          createTweetToast(data);
        }
    } catch (error) {}
};

socket.onclose = function (event) {
  console.log("Socket connection closed.");
};
