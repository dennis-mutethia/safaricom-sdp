
from src.sdp import SDP
from src.premium_sms import PremiumSMS
from src.exceptions.sdp_exception import SDPException


try:
    # Instantiate the SDP class, passing the API username, password, and cp_id
    sdp = SDP()

    # By default, SDP will use sandbox APIs. Call use_live() method to use production APIs.
    sdp.use_live().init()

    # Instantiate the PremiumSMS class and pass the SDP instance
    premium_sms = PremiumSMS(sdp)

    # Send SMS
    request_id = "1234"  # Generate an ID for tracking/logging purposes
    offer_code = "23456"  # The service for which the SMS is being sent
    link_id = "233348438989"  # ID generated when a user requests a service in SDP
    phone_number = "254712345678"  # The phone number of the user to receive the message
    message = "This is a test message"

    response = premium_sms.send_sms(request_id, offer_code, link_id, phone_number, message)

    # Check the response and log as necessary
    if response['success']:
        # Request sent successfully to SDP. Not to be confused with SMS delivery success
        if 'responseParam' in response['data']:
            if response['data']['responseParam']['status'] == 1:
                # Failed to send SMS
                print(f"SMS sending failed with status code {response['data']['responseParam']['statusCode']}. "
                      f"Error says: {response['data']['responseParam']['description']}")
            else:
                # SMS sending was successful
                print(response['data']['responseParam']['description'])
        else:
            # No response param sent back. Handle this for tracking
            print("Seems the response hasn't been sent. Best to assume the SMS failed to send.")
    else:
        # Failed to send the request, possibly due to network, authentication, authorization errors
        print(f"Sending request failed with message: {response['errorMessage']}")

except SDPException as ex:
    # Handle error logging here, most likely exceptions occur during token generation
    print(ex)
