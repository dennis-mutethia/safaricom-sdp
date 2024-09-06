from src.utils import Utils


def handle_callback():
    # Get the callback response
    response = Utils.get_callback()
    
    # Get the request ID. You can use this to query your database and update the status
    request_id = response.get('requestId', "")
    
    # Check the status of the callback
    if not response['success']:
        # Callback received has an error
        # Update the status to failed delivery with the error message
        print(response['errorMessage'])
    else:
        # Correct callback data
        data = response['data']
        
        # Check the delivery status
        status = data['responseParam']['status']
        
        if status != 0:
            # Failed to deliver message (e.g., when the user has no airtime or is not subscribed)
            print(data['responseParam']['description'])
        else:
            # Message successfully delivered
            # Update the request status as successful
            print(f"Request {request_id} successfully delivered")

if __name__ == "__main__":
    handle_callback()
