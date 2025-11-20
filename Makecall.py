import streamlit as st
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables
load_dotenv()

def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

# Twilio configuration
TWILIO_ACCOUNT_SID = get_secret("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = get_secret("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = get_secret("TWILIO_PHONE_NUMBER")

st.title("Simple Call App")

# Debug info
if not TWILIO_ACCOUNT_SID:
    st.error("Twilio credentials not found! Please check your .env file.")
else:
    st.success("Twilio credentials loaded.")

phone_number = st.text_input(
    "Enter Phone Number (Indian: +91)",
    value="+91",
    placeholder="+919876543210"
)

# Webhook URL input - user must provide
webhook_url = st.text_input(
    "Webhook URL",
    placeholder="https://your-domain.com/twilio/incoming-call"
)

if st.button("Make Call"):
    if not phone_number:
        st.warning("Please enter a phone number.")
    elif not webhook_url:
        st.warning("Please enter a webhook URL.")
    else:
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # Ensure phone number has country code (+91 for Indian numbers)
            formatted_number = phone_number.strip()
            if not formatted_number.startswith("+"):
                # If no country code, assume Indian number and add +91
                if formatted_number.startswith("91"):
                    formatted_number = "+" + formatted_number
                elif formatted_number.startswith("0"):
                    # Remove leading 0 and add +91
                    formatted_number = "+91" + formatted_number[1:]
                else:
                    # Add +91 prefix
                    formatted_number = "+91" + formatted_number

            # Make call using webhook URL
            call = client.calls.create(
                to=formatted_number,
                from_=TWILIO_PHONE_NUMBER,
                url=webhook_url
            )

            st.success(f"Call initiated successfully! Call SID: {call.sid}")

        except Exception as e:
            st.error(f"Failed to make call: {str(e)}")