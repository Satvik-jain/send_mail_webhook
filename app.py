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
    user_email = data.get("email")
    subject = data.get("subject", "Notification")
    message_body = data.get("message")

    if not user_email or not message_body:
        return jsonify({"error": "Email, subject, and message body are required!"}), 400

    formatted_message = f"""
    Subject: {subject}
    
    {message_body}
    """

    msg = Message(
        subject=subject,
        recipients=[user_email],
        body=formatted_message,
        sender = "satvik.jain@tariniconsulting.com"
    )

    mail.send(msg)
    return jsonify({"message": f"Email sent successfully to {user_email}!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


# import os
# import requests
# from flask import Flask, request, jsonify
# from flask_mail import Mail, Message
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)

# # Email Configuration
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USE_SSL"] = False
# app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
# app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
# app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

# mail = Mail(app)

# # # Fetch properties from external API
# # def fetch_properties(filters):
# #     url = "https://voice-agent-zoho.onrender.com/properties"
# #     response = requests.post(url, json={"filters": filters}, headers={"Content-Type": "application/json"})
# #     return response.json().get("result", []) if response.status_code == 200 else []

# @app.route("/send_email", methods=["POST"])
# def send_email():
#     """Send an email with property details."""
#     data = request.get_json()
#     user_email = data.get("email")
#     filters = data.get("filters", {})

#     if not user_email:
#         return jsonify({"error": "Email is required!"}), 400

#     properties = fetch_properties(filters)
    
#     if not properties:
#         return jsonify({"message": "No properties found for the given filters!"}), 404

#     message_body = "🏠 **Property Listings:**\n\n"
#     for prop in properties:
#         message_body += f"📍 {prop.get('Street_Address', 'N/A')}, {prop.get('City', 'N/A')}, {prop.get('Country', 'N/A')}\n"
#         message_body += f"🛏️ {prop.get('Bedrooms', 'N/A')} Bed | 🚿 {prop.get('Bathrooms', 'N/A')} Bath | 💰 Rent: {prop.get('Rent_per_month', 'N/A')} USD\n"
#         message_body += f"🏡 Furnished: {prop.get('Furnished', 'N/A')} | 🏊 Pool: {prop.get('Swimming_Pool', 'N/A')} | 🌳 Garden: {prop.get('Garden', 'N/A')}\n\n"

#     msg = Message(
#         subject="🏠 Your Property Listings!",
#         recipients=[user_email],
#         body=message_body
#     )

#     mail.send(msg)
#     return jsonify({"message": f"Email sent successfully to {user_email}!"})

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)
