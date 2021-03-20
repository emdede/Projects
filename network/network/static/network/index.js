document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.edit-button').forEach(button => {
        button.onclick = function() {
            show_edit(button.dataset.postid);
        };
    });

    console.log("Content loaded");
});

function show_edit(postid) {
    console.log(postid);
    document.querySelector(`#content-${postid}`).style.display = 'none';
    document.querySelector(`#editfield-${postid}`).style.display = 'block';
    const button = document.querySelector(`#editbutton-${postid}`);
    button.innerHTML = 'Save changes';
    button.onclick = function() {
        edit(postid);
    };
}

function edit(postid) {
    console.log('inside edit');
    fetch('/new', {
        method: "PUT",
        body: JSON.stringify({
            postid: postid,
            content: document.querySelector(`#editfield-${postid}`).value
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        document.querySelector(`#content-${postid}`).style.display = 'block';
        document.querySelector(`#content-${postid}`).innerHTML = result[0];
        document.querySelector(`#editfield-${postid}`).style.display = 'none';
        const button = document.querySelector(`#editbutton-${postid}`);
        button.innerHTML = 'Edit Post';
        button.onclick = function() {
            show_edit(postid);
        };
    });
}

function like(postid) {
    console.log('like');
    fetch('/like', {
        method: "POST",
        body: JSON.stringify({
            mode: "LIKE",
            postid: postid
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        document.querySelector(`#likes-${postid}`).innerHTML = result.newlikes;
        document.querySelector(`#like-${postid}`).innerHTML = "Unlike";
        document.querySelector(`#like-${postid}`).onclick = function() {
            unlike(postid);
        }
    })
}

function unlike(postid) {
    console.log('unlike');
    fetch('/like', {
        method: "POST",
        body: JSON.stringify({
            mode: "UNLIKE",
            postid: postid
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        document.querySelector(`#likes-${postid}`).innerHTML = result.newlikes;
        document.querySelector(`#like-${postid}`).innerHTML = "Like";
        document.querySelector(`#like-${postid}`).onclick = function() {
            like(postid);
        }
    })
}