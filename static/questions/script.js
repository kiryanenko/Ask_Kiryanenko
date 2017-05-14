function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function putLike(url, isLike, rating_id)
{
    var form = document.getElementById(rating_id);
    var like = document.getElementById('like_' + rating_id);
    var dislike = document.getElementById('dislike_' + rating_id);
    var request = $.ajax({
        url: url,
        type: 'POST',
        data: { is_like: isLike, csrfmiddlewaretoken: csrftoken },
        success: function(data) {
            if (data.status === 'ok') {
                rating.value = data.rating;
                like.disabled = true;
                dislike.disabled = true;
            }
        }
    })
}