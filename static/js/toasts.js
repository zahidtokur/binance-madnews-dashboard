const postToastCol = $(".post-toasts-col");
const tweetToastCol = $(".tweet-toasts-col");
const postSound = $("#postSound");
const tweetSound = $("#tweetSound");
var post_temp_id = 1;
var tweet_temp_id = 1;

function createPostToast(data) {
  // notification sound
  playPostNotificationSound(postSound.is(":checked"));

  // create outer div
  var toastDiv = document.createElement("div");
  toastDiv.classList.add("toast", "mb-2");
  toastDiv.id = "post_" + post_temp_id;
  toastDiv.setAttribute("data-bs-autohide", "false");

  // create toast header
  var toastHeader = document.createElement("div");
  toastHeader.classList.add("toast-header");
  toastHeader.classList.add("text-bg-warning");

  // create header elements
  var username = document.createElement("strong");
  username.innerText = data.source;
  username.classList.add("me-auto");
  var closeBtn = document.createElement("button");
  closeBtn.type = "button";
  closeBtn.setAttribute("data-bs-dismiss", "toast");
  closeBtn.classList.add("btn-close");

  // add header elements to header
  toastHeader.append(username);
  toastHeader.append(closeBtn);

  // add header to outer div
  toastDiv.append(toastHeader);

  // create toast body
  var toastBody = document.createElement("div");
  toastBody.classList.add("toast-body");
  toastBody.innerText = data.title;

  // create link to the post
  var linkDiv = document.createElement("div");
  linkDiv.classList.add("mt-2", "pt-2", "border-top");

  // create link
  var link = document.createElement("a");
  link.classList.add("btn", "btn-outline-dark", "btn-sm");
  link.target = "_blank";
  link.href = data.url;
  link.innerText = "Go to url";

  // add link to toast body
  linkDiv.append(link);
  toastBody.append(linkDiv);

  // add toast body to outer div
  toastDiv.append(toastBody);

  // add post to column
  postToastCol.prepend(toastDiv);

  // show toast
  var toast = bootstrap.Toast.getOrCreateInstance($("#post_" + post_temp_id));
  post_temp_id++;
  toast.show();
};

function createTweetToast(data) {
  // notification sound
  playTweetNotificationSound(tweetSound.is(":checked"));

  // create outer div
  var toastDiv = document.createElement("div");
  toastDiv.classList.add("toast", "mb-2");
  toastDiv.id = "tweet_" + data.info.twitterId;
  toastDiv.setAttribute("data-bs-autohide", "false");

  // create toast header
  var toastHeader = document.createElement("div");
  toastHeader.classList.add("toast-header");
  toastHeader.classList.add("text-bg-primary");

  // create header elements
  var username = document.createElement("strong");
  username.innerText = data.title;
  username.classList.add("me-auto");
  var closeBtn = document.createElement("button");
  closeBtn.type = "button";
  closeBtn.setAttribute("data-bs-dismiss", "toast");
  closeBtn.classList.add("btn-close");

  // add header elements to header
  toastHeader.append(username);
  toastHeader.append(closeBtn);

  // add header to outer div
  toastDiv.append(toastHeader);

  // create toast body
  var toastBody = document.createElement("div");
  toastBody.classList.add("toast-body");
  toastBody.innerText = data.body;

  // create link to the post
  var linkDiv = document.createElement("div");
  linkDiv.classList.add("mt-2", "pt-2", "border-top");

  // create link
  var link = document.createElement("a");
  link.classList.add("btn", "btn-outline-dark", "btn-sm");
  link.target = "_blank";
  link.href = data.link;
  link.innerText = "Go to tweet";

  // add link to toast body
  linkDiv.append(link);
  toastBody.append(linkDiv);

  // add toast body to outer div
  toastDiv.append(toastBody);

  // add post to column
  tweetToastCol.prepend(toastDiv);

  // show toast
  var toast = bootstrap.Toast.getOrCreateInstance(
    $("#tweet_" + data.info.twitterId)
  );
  toast.show();
};

function playPostNotificationSound(sound_on) {
  if (sound_on) {
    var sound = new Audio("static/assets/post_notification.wav");
    sound.play();
  }
};

function playTweetNotificationSound(sound_on) {
  if (sound_on) {
    var sound = new Audio("static/assets/tweet_notification.mp3");
    sound.play();
  }
};

$("#clearNotifications").click(function () {
  $('.toast').toast('hide');
});