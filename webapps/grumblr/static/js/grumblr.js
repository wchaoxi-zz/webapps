
function getUpdates() {
    var posts =$("#allposts");
    $.get("grumblr/getnewposts")
        .done(function(data) {
            for (var i = 0; i < data.posts.length; i++) {
                var new_post = $(data.posts[i].html);
                posts.prepend(new_post);
                // console.log(new_post);
                // console.log($(new_post.lastChild.lastChild));
                // $(new_post.lastChild.lastChild).click(comment);
            }
        });
}

function comment(e) {
    var content = $(e.target).prev();
    var id = $(e.target).parent().attr('id');
    var list = $(e.target).next();
    console.log("hi")
    $.post("/grumblr/addcomment/" + id, {comment : content.val()})
        .done(function (data) {
            var new_comment = $(data.html);
            list.append(new_comment);
            getUpdates();
        });
}



$( document ).ready(function() {
    $("#allposts").on("click", "button.comment", comment);

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  window.setInterval(getUpdates, 5000);

  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

});

