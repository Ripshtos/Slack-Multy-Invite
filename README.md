# Slack Chanell Multy adder/remover 
TLDR : Basiclly this code adds/removes the engineer to all the channels you're currently on (** Note the private parameter , i take no responsibilty if you added your engingeer to said private company insider groups **).

Every time a new engineer joins my team, I inevitably end up inviting said engineer to each Slack channel manually. I got tired of this.
Slack asks for more money after adding said engineer to a group ( for example @support ) so i made a cost effective script for your usage.

Enjoy!

## Instructions
1. [Create](https://api.slack.com/apps) a Slack App for your workspace.
2. Add the following permission scopes to a user token (bot tokens aren't allowed `channels:write`):
    - `users:read`
    - `users:read.email`
    - `channels:read`
    - `channels:write`
    - `groups:read` (only if inviting to private channels)
    - `groups:write` (only if inviting to private channels)
3. Install app to your workspace which will generate a new User OAuth token

Download my script:
git clone https://github.com/Ripshtos/slack-multi-invite

* Set private flag to true if you want to invite users to private channels. As noted above, this will require the additional permission scopes of groups:read and groups:write , set the api key to be the one you got from the slack app and set all other parameters according to the incode documentation ( add/remove ) etc...

For example :
Want to remove the engineer from all channels you're members at ?
Simply set the optional action flag to remove (add is the default):
 
