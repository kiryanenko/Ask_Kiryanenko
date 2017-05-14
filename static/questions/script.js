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
    var rating= form.getElementsByClassName('rating-input')[0];
    var like = form.getElementsByClassName('rating-like')[0];
    var dislike = form.getElementsByClassName('rating-dislike')[0];
    $.ajax({
        url: url,
        type: 'POST',
        data: { is_like: isLike, csrfmiddlewaretoken: csrftoken },
        success: function(data) {
            if (data.status === 'ok') {
                rating.value = data.rating;
                if (isLike) {
                    like.disabled = true;
                    dislike.disabled = false;
                } else {
                    like.disabled = false;
                    dislike.disabled = true;
                }
            }
        }
    })
}

function correctAnswer(url, answer_id)
{
    $.ajax({
        url: url,
        type: 'POST',
        data: { answer_id: answer_id, csrfmiddlewaretoken: csrftoken },
        success: function(data) {
            if (data.status === 'ok') {
                var labels = document.getElementsByClassName('correct_answer-description');
                for (var i = 0; i < labels.length; ++i) {
                    labels[i].innerHTML = 'Пометить как верный.';
                }
                document.getElementById('correct_answer-description-'+answer_id).innerHTML = 'Выбран как верный!'
            }
        }
    })
}
