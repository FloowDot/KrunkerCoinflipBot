Disclaimer: I dont usually use github and I have no clue how to write a readme file so this is gonna be a mess

A stripped down version of my krunker gambling bot I used to run.

This version of the bot only features the balance storing system (Anti-Scam) and the coinflipping system
If you would like to obtain access the to the full version of the bot (Levelling system, Lottery system, Roulette, Blackjack, Jackpot, Minesweeper, Crash, referall link system etc.) HMU on discord:
 .Floow#5852 (ID: 234888341789605888)

To get started you should make a discord bot application with send message permissions and embed permissions and add it to your server (To avoid the bot breaking with future updates its best to just tick all non moderation options)

Additionally, give the bot the Member intents.

I am currently using python 3.8.7 to develop the bot, so if you want to avoid issues I would suggest using that version (:

prerequisites are just discord.py (py -m pip install discord.py)

To get started, make the following channels/roles in your server (They can be named anything):

Deposit channel: (Where users will deposit their KR into their server account) - It is reccomended for people with the dealer role to turn on message notifications for this channel
Withdraw Channel: (Where users will withdraw their server KR into their krunker account) - It is reccomended for people with the dealer role to turn on message notifications for this channel
Command Channel: (This can be your pre existing bot command channel)
Coinflip Channel: (Where users will do the actually coinflipping)
Coinflip Log Channel: (Where all coinflip messages will be logged - Make sure this channel is visible to the bot)
Dealer Role: (The role that allows people to add/remove KR from other peoples balance. Give this to moderators/admins so they can handle deposits/withdraws :))

Now run the setup.py tool and fill in all the settings.

Now you are ready to run bot.py, existing members can set up their balance by doing .b in the command channel or coinflip channel. New members will automatically have their balance set up.

Command Documentation:

.balancereset <userid> <confirm> - Resets the balance of a user. <confirm>'s value should be 'confirm' (Admin only command)
.balance <user> - Checks the balance of the tagged user. Don't tag anyone to check your own balance
.deposit <amount> <ign> - Command used for a member to indicate they want to deposit
.withdraw <amount> <ign> - Command used for a member to indicate they want to withdraw and to what account (Automatically accounts for gift fees)
.link <ign> - Quickly creates a profile link
.add <amount> <user> - Adds/Subtracts <amount> KR to tagged users balance for depositting/withdrawing. (Use negative numbers to remove from balance) (Dealer only command)
.coinflip <action>
    .coinflip list - displays a list of coinflips to join
    .coinflip create <amount> - Creates a coinflip for <amount> on heads
    .coinflip join <user> - Joins tagged users coinflip (Automatically picks winner and sends KR)
    .coinflip cancel - Cancels current coinflip
.leaderboard - Shows a leaderboard of highest KR balances
