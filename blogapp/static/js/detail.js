function editComment(id){

    document.getElementById("text"+id).style.display="none";

    document.getElementById("textarea"+id).style.display="block";

    document.getElementById("edit"+id).style.display="none";

    document.getElementById("save"+id).style.display="inline-block";

    document.getElementById("cancel"+id).style.display="inline-block";

    // Mobile editing layout
    document.getElementById("comment"+id).classList.add("editing");
}

function cancelEdit(id){

    document.getElementById("textarea"+id).style.display="none";

    document.getElementById("text"+id).style.display="block";

    document.getElementById("edit"+id).style.display="inline-block";

    document.getElementById("save"+id).style.display="none";

    document.getElementById("cancel"+id).style.display="none";

    // Remove mobile editing layout
    document.getElementById("comment"+id).classList.remove("editing");
}

function saveComment(id){

    const text = document.getElementById("textarea" + id).value;

    fetch("/comment/update/" + id + "/", {

        method: "POST",

        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },

        body: "text=" + encodeURIComponent(text)

    })

    .then(response => {

        if (!response.ok) {
            throw new Error("Failed to update comment.");
        }

        return response.json();

    })

    .then(data => {

        document.getElementById("text" + id).innerHTML = data.text;

        cancelEdit(id);

    })

    .catch(error => {

        console.error(error);

        alert("Unable to update comment. Please try again.");

    });

}

function getCookie(name){

    let cookieValue = null;

    if(document.cookie && document.cookie !== ''){

        const cookies = document.cookie.split(';');

        for(let i=0;i<cookies.length;i++){

            const cookie = cookies[i].trim();

            if(cookie.substring(0,name.length+1) === (name + '=')){

                cookieValue = decodeURIComponent(cookie.substring(name.length+1));

                break;
            }

        }

    }

    return cookieValue;

}

function likeBlog(id) {

    fetch("/like/" + id + "/", {

        method: "POST",

        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }

    })

    .then(response => {

        if (!response.ok) {
            throw new Error("Failed to like blog.");
        }

        return response.json();

    })

    .then(data => {

        if (data.login) {

            window.location.href = "/login/";

            return;

        }

        document.getElementById("like-count").innerText = data.likes;

        const heart = document.getElementById("heart-icon");

        if (data.liked) {

            heart.classList.remove("fa-regular");
            heart.classList.add("fa-solid");

        } else {

            heart.classList.remove("fa-solid");
            heart.classList.add("fa-regular");

        }

    })

    .catch(error => {

        console.error(error);

        alert("Unable to update like. Please try again.");

    });

}