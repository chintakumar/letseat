from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_otp_sms(phone, otp):
    """
    Dummy SMS sender for OTPs.
    If Twilio credentials are set in .env, you can integrate Twilio.
    Otherwise, just log the OTP to console.
    """
    if (
        getattr(settings, "TWILIO_ACCOUNT_SID", "")
        and getattr(settings, "TWILIO_AUTH_TOKEN", "")
        and getattr(settings, "TWILIO_FROM_NUMBER", "")
    ):
        try:
            from twilio.rest import Client

            client = Client(
                settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
            )
            message = client.messages.create(
                body=f"Your LetsEat login OTP is {otp}",
                from_=settings.TWILIO_FROM_NUMBER,
                to=phone,
            )
            logger.info(f"OTP sent via Twilio: {message.sid}")
        except Exception as e:
            logger.error(f"Twilio send failed: {e}")
    else:
        # Fallback: just print OTP for testing
        print(f"DEBUG: OTP for {phone} is {otp}")
