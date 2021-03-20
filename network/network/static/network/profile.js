document.addEventListener('DOMContentLoaded', function() {

    let profile_id = JSON.parse(document.querySelector('#profile-id').textContent);
    let following = JSON.parse(document.querySelector('#currently-following').textContent);

    if (following) {
        document.querySelector('#unfollow').style.display = 'block';
    } else {
        document.querySelector('#follow').style.display = 'block';
    }

    // Follow request
    document.querySelector('#follow').addEventListener('click', () => {
        fetch(`${profile_id}/follow`, {
            method: "POST"
        })
        .then(result => {
            console.log(result)
            if(result.status === 200) {
                document.querySelector('#unfollow').style.display = 'block';
                document.querySelector('#follow').style.display = 'none';
                let follower_count = parseInt(document.querySelector('#follower-count').innerHTML); 
                document.querySelector('#follower-count').innerHTML = follower_count + 1;
            } else {
                alert("You are not logged in.");
            }
        });
    })
    // Unfollow request
    document.querySelector('#unfollow').addEventListener('click', () => {
        fetch(`${profile_id}/follow`, {
            method: "DELETE"
        })
        .then(result => {
            console.log(result)
            document.querySelector('#unfollow').style.display = 'none';
            document.querySelector('#follow').style.display = 'block';
            let follower_count = parseInt(document.querySelector('#follower-count').innerHTML); 
            document.querySelector('#follower-count').innerHTML = follower_count - 1;
        });
    })
    console.log('loaded');
})