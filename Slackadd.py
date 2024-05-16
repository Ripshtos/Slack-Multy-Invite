import requests
import json
import sys

CONVERSATIONS_INVITE_URL = "https://slack.com/api/conversations.invite"
CONVERSATIONS_KICK_URL = "https://slack.com/api/conversations.kick"
CONVERSATIONS_LIST_URL = "https://slack.com/api/conversations.list"
USERS_LOOKUP_BY_EMAIL_URL = "https://slack.com/api/users.lookupByEmail"

def main():
    api_token = "enter your api api_token" #Enter your api token
    action = "add" #Modify to add or remove from channels
    emails = "guy@facebook.io" #Team Members you want to add 
    channels_arg = "support" #Just leave it like this as itl automaticlly set this to your channels 
    private = "true" #Add to all private channels you're in or not
    debug = "true"

    if not api_token or not emails or not channels_arg or (action != "add" and action != "remove"):
        print("Invalid input")
        sys.exit(1)

    private = True if private.lower() == "true" else False
    debug = True if debug.lower() == "true" else False

    user_ids = []
    #finds and sets the slack user id's via email
  
    for email in emails.split(","):
        user_id = get_user_id(api_token, email)
        if user_id:
            print(f"Valid user (ID: {user_id}) found for '{email}'")
            user_ids.append(user_id)
        else:
            print(f"Error while looking up user with email {email}")

    if not user_ids:
        print("\nNo users found - aborting")
        sys.exit(1)

    #Gets your channel id's ( ADDS THE USER ALL THE CAHNNELS YOU ARE CURRENTLY ON )
    channels_map = get_channels(api_token, private, debug)
    channels = get_channels(api_token, private, debug)

    print("Channels:")
    for name, channel_id in channels.items():
        print(f"{name}")
        
    if debug:
        print(f"DEBUG: Total # of channels retrieved: {len(channels_map)}")

    if action == "add":
        print("Adding users to all channels found ...")
        for channel, channel_id in channels_map.items():
            invite_users_to_channel(api_token, user_ids, channel_id)
            print(f"Users added to channel '{channel}'")
            
    print("\nAll done! You're welcome =)")

def get_user_id(api_token, user_email):
    url = f"{USERS_LOOKUP_BY_EMAIL_URL}?email={user_email}"
    headers = {
        "Authorization": f"Bearer {api_token}",
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get("ok"):
        return data["user"]["id"]
    else:
        return None

def get_channels(api_token, private, debug):
    channel_type = "public_channel"
    if private:
        channel_type = "private_channel"

    name_to_id = {}

    next_cursor = ""
    while True:
        url = f"{CONVERSATIONS_LIST_URL}?cursor={next_cursor}&exclude_archived=true&limit=200&types={channel_type}"
        headers = {
            "Authorization": f"Bearer {api_token}",
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if debug:
            print(f"DEBUG: # of channels returned in page: {len(data['channels'])}")

        for channel in data["channels"]:
            name_to_id[channel["name"]] = channel["id"]

        next_cursor = data.get("response_metadata", {}).get("next_cursor")
        if not next_cursor:
            break

    return name_to_id

def invite_users_to_channel(api_token, user_ids, channel_id):
    url = CONVERSATIONS_INVITE_URL
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "channel": channel_id,
        "users": ",".join(user_ids),
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if not data.get("ok"):
        print(f"Error while inviting users to channel ({channel_id}): {data['error']}")

def remove_users_from_channel(api_token, user_ids, channel_id, debug):
    for user_id in user_ids:
        url = CONVERSATIONS_KICK_URL
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "channel": channel_id,
            "user": user_id,
        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if not data.get("ok") and debug:
            print(f"DEBUG: Error while removing user {user_id} from channel {channel_id}: {data['error']}")

if __name__ == "__main__":
    main()
