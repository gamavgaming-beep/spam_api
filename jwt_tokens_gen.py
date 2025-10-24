import json
import requests
import time
from threading import Thread

def get_jwt_tokens():
    # Load the account data
    with open('300_guest_account.json', 'r') as f:
        accounts = json.load(f)
    
    tokens = []
    
    # Process each account
    for uid, password in accounts.items():
        try:
            # Call the API to get the JWT token
            url = f"https://projects-fox-x-get-jwt.vercel.app/get?uid={uid}&password={password}"
            response = requests.get(url)
            
            if response.status_code == 200:
                token_data = response.json()
                if 'token' in token_data:
                    tokens.append({"token": token_data['token']})
                    print(f"Successfully got token for UID: {uid}")
                else:
                    print(f"Token not found in response for UID: {uid}")
            else:
                print(f"Failed to get token for UID: {uid}, Status code: {response.status_code}")
        
        except Exception as e:
            print(f"Error processing UID {uid}: {str(e)}")
    
    # Save the tokens to file
    with open('spam_me.json', 'w') as f:
        json.dump(tokens, f, indent=4)
    
    print(f"Saved {len(tokens)} tokens to spam_me.json")

def run_periodically():
    while True:
        get_jwt_tokens()
        # Wait for 8 hours (8 * 60 * 60 seconds)
        time.sleep(8 * 60 * 60)

if __name__ == "__main__":
    print("Starting JWT token generation...")
    
    # Run immediately first
    get_jwt_tokens()
    
    # Then run every 8 hours in a separate thread
    thread = Thread(target=run_periodically)
    thread.daemon = True
    thread.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script stopped by user")