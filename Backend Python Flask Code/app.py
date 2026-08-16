# ----------------------------------------------------------
# Main Server Code
# ----------------------------------------------------------

# --------------------------------------------
# Import Libaries
# --------------------------------------------

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from urllib.parse import parse_qs
from urllib.parse import parse_qsl
import mysql.connector
import os
import requests
import json
import secrets
import string

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("PORT"))

@app.route("/", methods=["GET", "POST"], strict_slashes=False)
@cross_origin()
def main():
  length = 128
  email_domain = "*main-backend-server-production.up.railway.app"
  version = "UMTS VERSION 1.0"
  
  sql_host1 = os.getenv("SQL_HOST")
  sql_username1 = os.getenv("SQL_USER")
  sql_password1 = os.getenv("SQL_PASS")
  sql_database_1 = os.getenv("SQL_DATABASE_1")
  sql_database_2 = os.getenv("SQL_DATABASE_2")
  
  acc_sql_database = mysql.connector.connect(
    host=sql_host1,
    user=sql_username1,
    password=sql_password1
    database=sql_database_1
  )
  
  ema_sql_database = mysql.connector.connect(
    host=sql_host1,
    user=sql_username1,
    password=sql_password1
    database=sql_database_2
  )
  
  acc_sql = acc_sql_database.cursor()

  if request.method == "POST":

    raw_text = request.data.decode('utf-8')

    clean_data = parse_qs(raw_text)
    tag_value = clean_data.get('tag', [None])[0]

    print(raw_text)

    if tag_value == "account-login":
        # Extracts Data from HTTP 

       raw_text = request.data.decode('utf-8')

       clean_data = parse_qs(raw_text)

      
       username = clean_data.get('username', [None])[0]
       password = clean_data.get('password', [None])[0]
      
       sql_check_acc_user = acc_sql.execute("SELECT Username FROM 'Account_details' WHERE Username = {username}, Password = {password}")
       sql_check_acc_pass = acc_sql.execute("SELECT Password FROM 'Account_details' WHERE Username = {username}, Password = {password}")
      
       # Tests login details to try and find a match

       if sql_check_acc_user == username:
        if sql_check_acc_pass == password:
          # Generates a new session ID
          new_session_id = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
          
          acc_sql.execute("UPDATE 'Account_details' SET Session_ID = {new_session_id} WHERE Username = {username}, Password = {password}")

          print("Sending Response")

          return jsonify({"session_id": new_session_id}), 200

        else:
          print("Authentication Failed: Incorrect Password")
          return jsonify({"status": "ERROR", "message": "INCORRECT PASSWORD"}), 401
       else:
        print("Authentication Failed: Username Not Found")
        return jsonify({"status": "ERROR", "message": "USERNAME NOT FOUND"}), 401

    elif tag_value == "account-signup":
      # Creates a new User

      with open("accounts.json", "r") as file:
        account = json.load(file)

      raw_text = request.data.decode('utf-8')

      clean_data = parse_qs(raw_text)

      username = clean_data.get('username', [None])[0]
      password = clean_data.get('password', [None])[0]

      if username in account:
        print("Error Creating User: Username Taken")
        return jsonify({"status": "ERROR", "message": "USERNAME TAKEN"}), 500

      elif "@test.co.uk" in username:
        print("Error Creating User: Invaild Username")
        return jsonify({"status": "ERROR", "message": "INVAILD USERNAME"}), 401

      else:
        new_user = {
          "password": password,
          "active_session_id": ""
        }

        account[username] = new_user

        with open("accounts.json", "w") as file:
          json.dump(account, file, indent=4)

        return jsonify({"status": "WORK", "message": "CREATED USER"}), 200

    elif tag_value == "send-email":

      raw_text = request.data.decode('utf-8')
      clean_data = parse_qs(raw_text)
      
      unique_length = 16

      receiver = clean_data.get('receiver', [None])[0]
      sender = clean_data.get('sender', [None])[0]
      message = clean_data.get('message', [None])[0]
      time = clean_data.get('time_sent', [None])[0]
      date = clean_data.get('date_sent', [None])[0]
      subject = clean_data.get('subject', [None])[0]
      token = clean_data.get('session_token', [None])[0]
      
      unique_string = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(unique_length))
 
      email_id = date + "#" + time + "#" + unique_string + "#" + email_domain 

      with open("accounts.json", "r") as file:
        account = json.load(file)

      if email_domain in receiver:

        if sender in account:
          if account[sender]["active_session_id"] == token:

            with open("emails.json", "r") as file:
              emailsfile = json.load(file)

            new_email = {
                "receiver": receiver,
                "sender": sender,
                "timestamp": time,
                "date-sent": date,
                "message": message,
                "subject": subject
              }

            emailsfile[email_id] = new_email

            with open("emails.json", "w") as file:
              json.dump(emailsfile, file, indent=4)

            print("Saved Email")
            return jsonify({"status": "WORK", "message": "SAVED EMAIL"}), 200

          else:
            print("Error: Invaild Session ID")
            return jsonify({"status": "ERROR", "message": "INVAILD SESSION ID"}), 401

        else:
          print("Error: Invaild Sender")
          return jsonify({"status": "ERROR", "message": "INVAILD SENDER"}), 500

      elif "*" in receiver:
        c = "*"

        domain_c = receiver.split(c, 1)
        domain = domain_c[1] if len(domain_c) > 1 else ""

        domain_real = f"http://{domain}/post"
        
        data_sent = f"tag=send-email-external&message=REQUEST CONNECTION"

        opening_connection = requests.post(domain_real, data_sent)

        res = dict(parse_qsl(opening_connection.text))

        if res.get("message") == "OPENED CONNECTION":
          print("Connection Opened")

          data_sent = f"tag=send-email-external&version={version}"

          version_connection = requests.post(domain_real, data_sent)

          res = dict(parse_qsl(version_connection.text))

          if res.get("message") == version:
            print("Confirmed Version Match")

            data_sent = f"tag=send-email-external&receiver={receiver}"

            receiver_connection = requests.post(domain_real, data_sent)
            res = dict(parse_qsl(receiver_connection.text))

            if res.get("message") == "CONFIRMED RECEIVER":
              print("Receiver Confirmed")

              data_sent = f"tag=send-email-external&receiver={receiver}&sender={sender}&message={message}&time_sent={time}&date_sent={date}&subject={subject}&id={unique_string}";

              data_connection = requests.post(domain_real, data_sent)
              res = dict(parse_qsl(data_connection.text))

              if res.get("message") == "RECEIVED DATA":
                print("Data Received")

                data_sent = f"tag=send-email-external&message=CLOSE CONNECTION"
                close_connection = requests.post(domain_real, data_sent)
                res = dict(parse_qsl(close_connection.text))

                if res.get("message") == "CLOSE CONNECTION":
                  print("Closing Connection")

                  return jsonify({"status": "ONLINE", "message": "EMAIL SENT TO EXTERNAL SERVER"}), 200

                else:
                  return jsonify({"status": "ERROR", "message": "FAILED TO CLOSE CONNECTION"}), 500

              else:
                return jsonify({"status": "ERROR", "message": "FAILED TO RECEIVER DATA CONFIRMATION"}), 500

            else:
              return jsonify({"status": "ERROR", "message": "FAILED TO CONFIRM RECEIVER OR RECEIVER DOES NOT EXIST AT DOMAIN ADDRESS"}), 500

          else:
            return jsonify({"status": "ERROR", "message": "FAILED TO CONFIRM VERSION OR VERSION MISMATCH"}), 500

        else:
          return jsonify({"status": "ERROR", "message": "FAILED TO OPEN CONNECTION"}), 500
      
      else:
        return jsonify({"status": "ERROR", "message": "EXTERNAL RECEIVER USES OTHER PROTOCAL THAN UMTS"}), 500

    elif tag_value == "get-data":

      raw_text = request.data.decode('utf-8')
      clean_data = parse_qs(raw_text)

      token = clean_data.get('session_id', [None])[0]
      username = clean_data.get('username', [None])[0]

      with open("accounts.json", "r") as file:
        account = json.load(file)

      if username in account:
        if account[username]["active_session_id"] == token:
          return jsonify({"name": username}), 200
        else:
          return jsonify({"name": ""}), 200
      else:
        return jsonify({"name": ""}), 200

    elif tag_value == "get-all-emails":

      token = clean_data.get('session_token', [None])[0]
      username = clean_data.get('username', [None])[0]

      with open("accounts.json", "r") as file:
        account = json.load(file)

      if username in account:
        if account[username]["active_session_id"] == token:

          with open("emails.json", "r") as file:
            email_all = json.load(file)

          all_id = []
          target_receiver = username

          for key, value in email_all.items():
            if value.get("receiver") == target_receiver:
              all_id.append(key)

          found_all = 0
          length_1 = (len(all_id))     
          temp = 0
          all_emails = {}

      
          while temp != length_1:
            temp_id = all_id[temp]
            temp_email = email_all[temp_id]
            
            all_emails[temp_id] = temp_email
            temp = temp + 1

          print(all_emails)
          final_message = {}

          other_info = {"total_num_emails": length_1}
          other_info2 = {"all_email_id": all_id}

          final_message = other_info | other_info2
          final_message = final_message | all_emails

          return jsonify(final_message), 200

        return jsonify({"status": "ERROR", "message": "INVALID SSID"}), 401

      return jsonify({"status": "ERROR", "message": "INVALID USERNAME"}), 401

    elif tag_value == "get-single-emails":

      raw_text = request.data.decode('utf-8')
      clean_data = parse_qs(raw_text)

      token = clean_data.get('session_token', [None])[0]
      username = clean_data.get('username', [None])[0]
      mail_id = clean_data.get('email_id', [None])[0]

      with open("accounts.json", "r") as file:
        account = json.load(file)

      if username in account:
        if account[username]["active_session_id"] == token:
          
          with open("emails.json", "r") as file:
            email_all = json.load(file)
            
          email = email_all[mail_id]

          return jsonify(email), 200

        return jsonify({"status": "ERROR", "message": "INVALID SSID"}), 401
        
      return jsonify({"status": "ERROR", "message": "INVALID USERNAME"}), 401

  elif request.method == "GET":
    return "D"
    pass

  return jsonify({"status": "ERROR", "message": "HTTP METHOD NOT ALLOWED"}), 405

# --------------------------------------------
# Main Code
# --------------------------------------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, threaded=True)
