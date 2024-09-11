
import os
from dotenv import load_dotenv

from src.sdp import SDP
from src.bulk_sms import BulkSMS
from src.exceptions.sdp_exception import SDPException

load_dotenv()


try:
    # Instantiate the SDP class with the API username, password, and cp_id
    sdp = SDP()

    # By default, SDP will use sandbox APIs. Call use_live() method to use production APIs.
    sdp.use_live().init()
    #sdp.init()

    # Instantiate the BulkSMS class and pass the SDP instance
    bulk_sms = BulkSMS(sdp)

    # Send SMS
    request_id = "1234"  # Generate an ID for tracking/logging purposes
    username = os.getenv('API_USERNAME')  # Username allocated by SDP after successful registration
    package_id = ""  # Campaign package ID issued upon successful registration
    originating_address = "test"  # Originating address assigned to partner
    recipients = ["254759697757"]
    message = "This is a bulk SMS"
    callback = os.getenv('BULK_SMS_CALLBACK_URL')

    response = bulk_sms.send_sms(request_id, username, package_id, originating_address, recipients, message, callback)

    # Check the response and log as necessary
    if response['success']:
        # Request sent successfully to SDP. This does not mean the bulk SMS has been sent to users
        if 'data' in response:
            if response['data']['status'] == "SUCCESS":
                # Bulk SMS successfully dispatched. Confirmation is awaited from the callback
                print("Messages successfully dispatched to SDP")
            else:
                # Error dispatching bulk SMS to SDP/Safaricom
                print(str(response))
                print(f"Failed to dispatch bulk SMS. Response code: {response['data']['statusCode']}")
        else:
            # No response param sent back. Handle this for tracking
            print("Response seems incomplete. Best to assume it failed to dispatch the bulk SMS.")
    else:
        # Failed to send the request, possibly due to network, authentication, or authorization errors
        print(f"Failed to send request. Error message: {response['errorMessage']}")

except SDPException as ex:
    # Handle error logging here, exceptions most likely occur during token generation
    print(ex)
