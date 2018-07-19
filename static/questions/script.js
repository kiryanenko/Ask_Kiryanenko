function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function putLike(url, isLike, rating_id)
{
    const form = document.getElementById(rating_id);
    const rating = form.getElementsByClassName('rating-input')[0];
    const like = form.getElementsByClassName('rating-like')[0];
    const dislike = form.getElementsByClassName('rating-dislike')[0];
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
                const labels = document.getElementsByClassName('correct_answer-description');
                for (let i = 0; i < labels.length; ++i) {
                    labels[i].innerHTML = 'Пометить как верный.';
                }
                document.getElementById('correct_answer-description-'+answer_id).innerHTML = 'Выбран как верный!'
            }
        }
    })
}

function connectToQuestionChannel(question_id) {
    const chatSocket = new WebSocket('ws://' + window.location.host + '/questions/' + question_id + '/');

    chatSocket.onmessage = function(e) {
        console.log(e.data);
        const data = JSON.parse(e.data);

    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
}
