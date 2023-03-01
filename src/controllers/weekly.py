import datetime
import math


class WeeklyVoteController:
    # 3 messages one with difficulty, one with the gamemode, one with the headers
    async def weeklyVoteMessage(self):
        return

    # final message created from the vote
    async def weeklyFinalMessage(self):
        return


    #message reminding about the vote
    async def weeklyReminderMessage(self, channel):
        weekly_time = datetime.datetime.today()
        weekly_time = weekly_time.replace(hour=20, minute=00, second=00)
        await channel.send(f"Weekly will be happening <t:{math.floor(weekly_time.timestamp())}:R> Don't forget to vote: *insert the vote link here*")