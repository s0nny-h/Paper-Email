function get_session_id() {
    let name = "session_id"
    const cookieString = document.cookie;
    const cookies = cookieString.split(";");
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

function get_username() {
    let name = "username"
    const cookieString = document.cookie;
    const cookies = cookieString.split(";");
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

function auth_check() {
    session_id = get_session_id()
    username = get_username()

    if (session_id == null) {
        console.log("ERROR: NIL SSID")
        window.location.replace("login.html");
    }
    else if (username == null) {
        console.log("ERROR: NIL USERNAME")
        window.location.replace("login.html");
    }
    else {
        const data = `tag=get-data&session_id=${session_id}&username=${username}`;

        fetch("https://main-backend-server-production.up.railway.app/", {
            method: "POST",
            headers: {
                "Content-type": "text/plain"
            },
            body: data
        })
        .then(function(response) {
            console.log("Status: ", response.status);
            return response.text()
        })
        .then(function(text) {
            const name = JSON.parse(text)

            if (name["name"] == "") {
                console.log("ERROR: AUTH FAILURE")
                window.location.replace("login.html");
            }
            else {
                document.getElementById("welcome").innerText = ("Logged In as: " + name["name"])
            }
        })
        .catch(function(error) {
            console.error("FETCH ERROR: ", error);
        })
    }
}

function login(e) {
    if (e) e.preventDefault();

    let username1 = document.getElementById("3").value
    let password1 = document.getElementById("4").value

    const details = {
        username: username1,
        password: password1,
        tag: "account-login"
    };

    const true_details = `username=${username1}&password=${password1}&tag=account-login`;

    document.cookie = ("username=" + username1)

    fetch("https://main-backend-server-production.up.railway.app/", {
        method: "POST",
        headers: {
            "Content-type": "text/plain"
        },
        body: true_details            
    })
    .then(function(response) {
        console.log("SESSION ID RECIVED");
        console.log("Status: ", response.status);
        return response.text()
    })
    .then(function(text) {
        const session_id = JSON.parse(text)

        document.cookie = ("session_id=" + session_id["session_id"]);

        window.location.replace("index.html");
    })
    .catch(function(error) {
        console.error("FETCH ERROR: ", error);
    })
}   

function sign_up(e) {
    if (e) e.preventDefault();
    let username1 = document.getElementById("5").value
    let password1 = document.getElementById("6").value

    const details = {
        username: username1,
        password: password1,
        tag: "account-signup"
    };

    const true_details = `username=${username1}&password=${password1}&tag=account-signup`;

    fetch("https://main-backend-server-production.up.railway.app/", {
        method: "POST",
        headers: {
            "Content-type": "text/plain"
        },
        body: true_details            
    })
}

function send_email(event) {
    if (event) event.preventDefault();
    window.location.replace("send_email.html");
}

function read_email(event) {
    if (event) event.preventDefault();
    window.location.replace("read_email.html");
}

function log_out(event) {
    if (event) event.preventDefault();
    document.cookie = "username=";
    document.cookie = "session_id=";
    window.location.replace("login.html");
}

function home_page(event) {
    if (event) event.preventDefault();
    window.location.replace("index.html");
}

function delete_account(event) {
    if (event) event.preventDefault();
    window.alert("Placeholder")
}
