"pip3 install pandas"
"python3 script.py"
"output csvs sanitized/"

Note: There is <1% chance the script throws an assertion error.
Shouldn't happen, but if it does, just run it again.

There are 1000 users, user_names are unique.
All users have a telegram_handle. telegram_handles are unique.
There are 50 organisation, organisation_names, organisation_emails are unique.
There are 50 boards, every user belongs to exactly 4 boards.
board_names are unique.
There are 200 lists, list_names are unique.
There are 11 list_labels, namely - "top-priority, urgent, unimportant, external, estimates, backend, frontend, database, ui, ux, contractors"
There are 800 cards, card_names are unique.
There are 4 cards in every list. card_admins are the same as the corresponding list_admins.
There are 50 announcements
All 50 announcements are made by a single board_admin each.
Multiple cards, announcements may have the same multimedia_id.
There are 800 comments, one on every card by the card_admin
There are 800 multimedia objects.
Create the MOVE table yourself.
The MOVE table will be intially empty.