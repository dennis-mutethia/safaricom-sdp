
from src.sdp import SDP
from src.subscription import Subscription
from src.exceptions.sdp_exception import SDPException


try:
    # Instantiate the SDP class, passing the API username, password, and cp_id
    sdp = SDP()

    # By default, SDP will use sandbox APIs. Call use_live() method to use production APIs.
    #sdp.use_live().init()
    sdp.init()

    # Instantiate the Subscription class and pass the SDP instance
    subscription = Subscription(sdp)

    # Activate subscription
    request_id = "1234"  # Generate an ID for tracking/logging purposes
    offer_code = "23456"  # The service for which the subscription is being activated
    phone_number = "254712345678"  # The phone number of the user

    response = subscription.activate_subscription(request_id, offer_code, phone_number)

    # Check the response and log as necessary
    if response['success']:
        # Request sent successfully to SDP. Not to be confused with the subscription activation success
        if 'responseParam' in response['data']:
            if response['data']['responseParam']['status'] == 1:
                # Failed to activate subscription
                print(f"Activation failed. Status code: {response['data']['responseParam']['statusCode']}. "
                      f"Error says: {response['data']['responseParam']['description']}")
            else:
                # Subscription activation success
                print(response['data']['responseParam']['description'])
        else:
            # No response param sent back. Handle this for tracking
            print("Response seems incomplete. Best to assume the activation failed.")
    else:
        # Failed to send the request, possibly due to network, authentication, or authorization errors
        print(f"Failed to send the request. Error message: {response['errorMessage']}")

except SDPException as ex:
    # Handle error logging here, most likely exceptions occur during token generation
    print(ex)
