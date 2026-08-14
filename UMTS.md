# Unique Mail Transfer System

## Server Communication Format

### Opening the connection

<server 1> REQUEST CONNECTION

<server 2> OPENED CONNECTION

This opens the connection to the other server (this doesnt actual open a connection it just preps the other server to be ready to receive any data sent)

### Show Verison of UMTS 

<server 1> UMTS VERSION: 1.0 (or any other version)

<server 2> UMTS VERSION: 1.0 (or any other version)

Both servers UMTS version must match for the data transfer to continue

### Check Receiver Exists on other server

<server 1> RECEIVER: {insert receiver here like: testing*test.co.uk}

<server 2> CONFIRMED RECEIVER

If the receiver does not exist then the other server needs to reply with any other response than "CONFIRMED RECEIVER" as this will force the servers to stop expecting more data to be sent

### Send Email Data

<server 1> DATA: {insert data here}

<server 2> RECEIVED DATA

The data that is sent show match this format here:

"tag=send-email-external&receiver={receiver}&sender={sender}&message={message}&time_sent={time}&date_sent={date}&subject={subject}&id={unique_string}"

### Closing the connection

<server 1> CLOSE CONNECTION

<server 2> CLOSE CONNECTION

This just tells both servers that they should stop expecting to get any more data from the other server.

## Notes

UMTS uses plaintext to communicate with the other server and expects plaintext to be sent back.

As of the code published on this Repo the UMTS has **NOT BEEN TESTED** however should work in theory, as well as this the code cannot as of right now receive any data from external server domains..
