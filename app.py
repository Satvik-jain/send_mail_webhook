import os
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Email Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

mail = Mail(app)

@app.route("/send_email", methods=["POST"])
def send_email():
    """Send an email with a properly formatted subject and message body."""
    data = request.get_json()
    data = data.get("args")
    user_email = data.get("email")
    subject = data.get("subject", "Notification")
    message_body = data.get("message")

    if not user_email or not message_body:
        return jsonify({"error": "Email, subject, and message body are required!"}), 400

    formatted_message = f"""{message_body}"""

    msg = Message(
        subject=subject,
        recipients=[user_email],
        body=formatted_message,
        sender=app.config["MAIL_DEFAULT_SENDER"]
    )

    mail.send(msg)
    return jsonify({"message": f"Email sent successfully to {user_email}!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
