# Paper Email
A fully custom Email web based client that uses a custom Email Transfer Protocol called UMTS (Unique Mail Transfer System) that handles emails being sent between email servers, hosted using GitHub Pages and a backend server that handles authentication and email transfer between servers and clients. As well as this the email address format uses: test*test.co.uk (this email is not registered)

The Paper Email website can be found at: https://s0nny-h.github.io/Paper-Email/

# Note
When signing up ensure that you put *main-backend-server-production.up.railway.app at the end of your username

# Status
This project is NOT COMPLETE. The following features are incomplete:
- Sending emails to external servers (this is not tested so it may work),
- Receving emails from external servers,

However emails can be sent and received if they are internal, and emails can be read. As well as this, the account login and signup system is fully complete.

# Authentication
This email client uses session ID's stored in cookies to authenticate users, as well as this any major request to the server will require the session ID otherwise you will be redirected to the login page.

# UMTS Protocol
UMTS (Unique Mail Transfer System) uses a custom email transfer protocal that I made for this project, the protocol uses the following for when communicating with other email servers:

<Server 1> REQUEST CONNECTION

*<server 2> OPENED CONNECTION*

<Server 1> UMTS VERSION: {insert version here}

*<server 2> UMTS VERSION: {insert version here}*

<Server 1> RECEIVER: {insert receiver}

*<server 2> CONFIRMED RECEIVER*

<Server 1> DATA: {insert email here}

*<server 2> RECEIVED DATA*

<Server 1> CLOSE CONNECTION

*<server 2> CLOSE CONNECTION*

The Email data that sent to external servers uses the format on the current server included in this GitHub Repo: 

tag=send-email-external&receiver={receiver}&sender={sender}&message={message}&time_sent={time}&date_sent={date}&subject={subject}&id={unique_string}

The UMTS versions must match for the transfer to be complete, as well as this all other server must reply with these exact responses.

More infomation on UMTS can be found in the "UMTS.md" file.

# Privacy

This email client and service collects the following data on users:
- Email addresses (registered to this service),
- Passwords (registered to this service),
- Session ID (registered to this service).

If you would like an account removal as of right now please email me at: sonny-harrison@outlook.com, this is because the account removal section of the main page is incomplete. As well as thia, feel free to contact me with any other questions about the project.

# Project Notes
This project would not be possible without half the internets web design tutorials and python flask tutorials, thank you to all inernet tutorials. 

As well as this, the client web side code alone is ~550 lines of code. And the server side code is ~330 lines. The code published has the "accounts.json" file empty and the "emails.json" file empty for security/privacy reasons

This project is not compatible with SMTP or any other email protocal as of right now, feel free to add to the code and host your own email provider using UMTS.

Ensure that you update/fill out all instances where a HTTP request is sent with your server address and on the server code "app.py" domain name needs to have: *{server address here} (example: *testing.co.uk).
