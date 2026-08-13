function close_email(email_id) {
    const dialog = document.getElementById("dialog-1")
    dialog.remove(); 
}

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

function open_email(buttonClass) {
    if (event) event.preventDefault();

    let username = get_username()
    let tag = "get-single-emails"
    let session_token = get_session_id()
    let email_id = buttonClass

    const data = `tag=${tag}&username=${username}&email_id=${email_id}&session_token=${session_token}`;

    fetch("", {
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
        const email = JSON.parse(text);

        let receiver = email["receiver"];
        let sender = email["sender"];
        let timestamp = email["timestamp"];
        let date_sent = email["date-sent"];
        let message = email["message"];
        let subject = email["subject"];

        const dialog = document.createElement("DIALOG");
        const br_1 = document.createElement("BR");
        const br_2 = document.createElement("BR");
        const br_3 = document.createElement("BR");
        const br_4 = document.createElement("BR");
        const br_5 = document.createElement("BR");
        const br_6 = document.createElement("BR");
        const br_7 = document.createElement("BR");
        const br_8 = document.createElement("BR");

        const button = document.createElement("BUTTON")

        const data_1 = document.createTextNode("Sender: " + sender + " ");
        const data_2 = document.createTextNode("Receiver: " + receiver + " ");
        const data_3 = document.createTextNode("Time Sent: " + timestamp + " ");
        const data_4 = document.createTextNode("Date Sent: " + date_sent + " ");
        const data_5 = document.createTextNode("Subject: " + subject + " ");
        const data_6 = document.createTextNode("Message: " + message + " ");

        dialog.setAttribute("open", "open");
        dialog.id = "dialog-1"
        button.textContent = "X";
        button.className = "close_email";

        button.onclick = function() { 
            close_email(email_id);
        };

        dialog.appendChild(button)
        dialog.appendChild(br_8)
        dialog.appendChild(data_1);
        dialog.appendChild(br_1);
        dialog.appendChild(data_2);
        dialog.appendChild(br_2);
        dialog.appendChild(data_3);
        dialog.appendChild(br_3);
        dialog.appendChild(data_4);
        dialog.appendChild(br_4);
        dialog.appendChild(br_6);
        dialog.appendChild(data_5);
        dialog.appendChild(br_7);
        dialog.appendChild(br_5);
        dialog.appendChild(data_6);

        document.body.appendChild(dialog);
    })
    .catch(function(error) {
        console.error("FETCH ERROR: ", error);
    })
}

function get_all_email(event) {
    if (event) event.preventDefault();

    let username = get_username()

    let tag = "get-all-emails"
    let session_token = get_session_id()

    const data = `tag=${tag}&username=${username}&session_token=${session_token}`;

    fetch("", {
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
        const all_emails = JSON.parse(text)

        let temp = 0;
        let total_num = all_emails["total_num_emails"];
        const all_email_id = all_emails["all_email_id"];

        while (temp != total_num) {
            let temp_id = all_email_id[temp];
            const temp_email = all_emails[temp_id];

            let sender = temp_email["sender"];
            let subject = temp_email["subject"];

            var paragraph = document.createElement("P");
            var button = document.createElement("BUTTON");
            var div1 = document.createElement("DIV");
            var div2 = document.createElement("DIV");

            div1.id = "div-2";
            div2.id = "emails";
            //button.id = "read_email";
            button.className = temp_id + " read_email";
            button.onclick = function() { 
                open_email(temp_id); 
            };
            button.textContent = "Read Email";
            div1.style.marginBlock = "20px";

            const data = document.createTextNode("From: " + sender + " | " + "Subject: " + subject);

            paragraph.appendChild(data);
            div1.appendChild(paragraph);
            paragraph.appendChild(button);
            div2.appendChild(div1);

            const element = document.getElementById("div-1");
            const p_start = document.getElementById("p-start"); 
            element.insertBefore(div1, p_start);

            temp = temp + 1;
        }

        temp = 0;
    })
    .catch(function(error) {
        console.error("FETCH ERROR: ", error);
    })
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

        fetch("", {
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
                get_all_email(event)
            }
        })
        .catch(function(error) {
            console.error("FETCH ERROR: ", error);
        })
    }
}

function compose_message(event) {
    if (event) event.preventDefault();

    let receiver = document.getElementById("1").value
    let message = document.getElementById("2").value
    let subject = document.getElementById("3").value
    let sender = get_username()

    let tag = "send-email"
    let session_token = get_session_id()

    const now = new Date();

    const time = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
    const date = now.getFullYear() + ":" + (now.getMonth() + 1) + ":" + now.getDate();

    const email = `tag=${tag}&receiver=${receiver}&sender=${sender}&message=${message}&time_sent=${time}&date_sent=${date}&subject=${subject}&session_token=${session_token}`;

    fetch("", {
        method: "POST",
        headers: {
            "Content-type": "text/plain"
        },
        body: email            
    })

    window.alert("Your Email was sent successfully!");
}

function home_page(event) {
    if (event) event.preventDefault();
    window.location.replace("index.html");
}