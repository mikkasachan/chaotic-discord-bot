from __future__ import annotations

import random

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import embed, member_name


CASE_TITLES = (
    "The People vs. Unnecessary Confidence",
    "State of the Server vs. Bro Trust Me",
    "The Great Group Chat Dispute",
    "Operation: Who Started This Kalesh?",
    "The Case of the Missing Common Sense",
    "The Republic vs. Suspicious Vibes",
    "The Court of Unfinished Side Quests",
    "The Legendary Matter of Too Much Aura",
)

ACCUSATIONS = (
    "server mein bina permission ke 17 baar 'bro trust me' bola.",
    "group chat mein 'guys suno' likh ke actual point kabhi nahi bataya.",
    "ek simple poll ko national election jaisa serious bana diya.",
    "apni hi galti ko lag ke naam se launch kar diya.",
    "online aake sabko ignore kiya, phir bola 'koi active nahi hai'.",
    "ek joke ko explain karke uski jaan le li.",
    "3 AM par bina context ke sirf 'interesting' message bheja.",
    "apne skill issue ko strategy bolne ki koshish ki.",
    "server ke snacks ko imaginary tax ke naam par confiscate kiya.",
    "reply karne se pehle teen business days ka notice manga.",
    "voice chat mein mic check ko full concert bana diya.",
    "ek hi story ko itna retell kiya ki lore khud confuse ho gaya.",
    "Google Maps ke saamne bhi directionally lost rehne ka record banaya.",
    "har discussion mein 'actually' bolkar facts ko vacation par bheja.",
    "apni aura ko itna hype kiya ki reality ne disclaimer laga diya.",
    "group project mein sirf 'mujhe koi bhi role de do' bolkar gayab ho gaya.",
    "notification dekh kar reply ka trailer release kiya, movie kabhi nahi aayi.",
    "ek harmless debate ko Kalesh Cinematic Universe bana diya.",
    "apne braincells ko alag-alag time zones mein kaam karne bheja.",
    "same meme ko naye caption ke saath historical discovery bataya.",
    "server mein bina warrant ke cringe reaction spam kiya.",
    "common sense ko 'optional setting' samajhkar disable kar diya.",
    "apni planning ko Google Calendar se bhi chhupa diya.",
    "ek chhoti si baat par dramatic background music imagine kiya.",
    "online status ko evidence samajhkar poori investigation chala di.",
    "apne comeback ko itna late bheja ki topic ka sequel aa gaya.",
    "NPC dialogue repeat karke usse personality development declare kiya.",
    "ek typo ko defend karte karte alternate timeline bana di.",
    "server ki shanti ko 'boring content' bolkar unnecessary chaos summon kiya.",
    "apni taraf se final answer dekar phir question hi badal diya.",
    "loading screen ko dekhkar patience naam ki cheez ko uninstall kar diya.",
)

EVIDENCE = (
    "ek suspicious screenshot aur 3 log jo kuch bhi yaad nahi rakhte.",
    "voice note jisme sirf background fan aur ek dramatic sigh hai.",
    "group chat ka timestamp jo khud suspicious lag raha hai.",
    "ek blurry reaction emoji aur bahut zyada confidence.",
    "witness ka statement: 'bhai vibes toh weird thi'.",
    "server logs ka ek imaginary page, highlighted in neon.",
    "ek deleted draft jisme 14 baar 'actually' likha tha.",
    "do confused pigeons aur ek strongly worded sticky note.",
    "ek poll jisme 100% voters ne 'kalesh' choose kiya.",
    "defendant ka status: online, par accountability offline.",
    "ek loading icon jo incident ke baad se rotate kar raha hai.",
    "chat mein teen consecutive 'bro' messages, context abhi missing hai.",
    "ek reaction chain jo court reporter bhi decode nahi kar paaya.",
    "screenshots ke screenshots ki ek suspiciously long family tree.",
    "ek witness jo kehta hai 'maine dekha tha', par details zero hain.",
    "aura meter ka handwritten result: 'bhai, kuch toh gadbad hai'.",
    "ek calendar invite titled 'urgent nonsense sync'.",
    "a mysterious snack wrapper found near the scene of the vibes.",
    "defendant ki planning sheet, jisme pehla step hi 'figure it out' hai.",
    "ek NPC dialogue loop aur uske neeche 'please help' reaction.",
)

PROSECUTION = (
    "Your Honor, is bande ki aura already questionable hai.",
    "Prosecution ka kehna hai ki vibes innocent nahi, bas well-formatted hain.",
    "Evidence kam hai, lekin confidence suspiciously zyada hai.",
    "Yeh normal skill issue nahi, premium subscription wala skill issue hai.",
    "Court ko bas defendant ka 'trust me' sunna hai; case khud samajh aa jayega.",
    "Is case mein logic witness box mein aaya tha, par jaldi chala gaya.",
    "Prosecution respectfully submit karti hai ki chaos intentional lag raha hai.",
    "Defendant ne facts ko seen karke vibes ko reply kiya hai.",
    "Server ki shanti ke khilaaf yeh ek highly creative conspiracy hai.",
    "Your Honor, itni confidence ke saath galat hona bhi ek talent hai.",
    "Yeh banda alibi bhi probably group chat se copy-paste karega.",
    "Prosecution ke paas proof nahi, par screenshots ka attitude hai.",
    "Defendant ka defense abhi loading mein hai, jo kaafi telling hai.",
    "Is case mein braincells ko summon kiya gaya tha; koi attend nahi hua.",
    "Aap sirf defendant ki typing dekhiye, baaki verdict automatic ho jayega.",
    "Kalesh itna obvious hai ki NPCs bhi side le rahe hain.",
    "Hum keh rahe hain: galti chhoti thi, drama ka production budget bada tha.",
    "Server ke collective vibes ne defendant ko already side-eye de diya hai.",
    "Yeh koi misunderstanding nahi, misunderstanding ka director's cut hai.",
    "Prosecution requests one thing: defendant ko thoda grass touch karne bheja jaye.",
)

DEFENSE = (
    "Mere client ne sirf skill issue kiya hai. Crime nahi hai.",
    "Defense ka kehna hai ki defendant ka brain abhi buffering par tha.",
    "Yeh intentional nahi tha; braincells ne emergency leave li thi.",
    "Mere client ko context diya hi nahi gaya, sirf vibes di gayi thi.",
    "Defendant innocent hai, bas uska decision tree thoda adventurous hai.",
    "Yeh kalesh nahi, ek badly planned side quest tha.",
    "Mere client ne 'trust me' bola tha, par warranty card nahi mila.",
    "Defense submits that the aura was misunderstood and the Wi-Fi was unstable.",
    "Defendant ka intention wholesome tha, execution ne plot twist kar diya.",
    "Mere client ko guilty nahi, tutorial ki zaroorat hai.",
    "Is poore case mein sabse zyada suspicious cheez prosecution ka confidence hai.",
    "Defendant bas main character moment try kar raha tha; script weak thi.",
    "Mere client ne facts ko ignore nahi kiya, unhe time to process diya.",
    "Yeh ek innocent typo tha jo group chat ne cinematic bana diya.",
    "Defense ke mutabik witness khud 3 AM par online tha, credibility questionable hai.",
    "Mere client ke braincells present the, bas attendance sheet galat thi.",
    "Agar weird vibes crime hain, toh poora server guilty hai.",
    "Defendant ne apology type ki thi, send button ne dhokha de diya.",
    "Mere client ka plan solid tha, reality ne cooperate nahi kiya.",
    "Defense asks the court to consider: at least chaos entertaining tha.",
)

VERDICTS = (
    "GUILTY. Court ne unanimously decide kiya: aura ka audit zaroori hai.",
    "NOT GUILTY. Lekin vibes ko 24 ghante observation mein rakha jayega.",
    "GUILTY with an asterisk. Asterisk ka meaning court bhi nahi jaanta.",
    "Case dismissed. Judge ko bhi context samajh nahi aaya.",
    "GUILTY of being iconic, innocent of everything else.",
    "Hung jury. Sab log evidence dekhte-dekhte snacks khane lage.",
    "NOT GUILTY, but defendant ka NPC license temporarily suspend hai.",
    "GUILTY. Skill issue ko official server incident declare kiya gaya.",
    "Court finds both parties dramatic, which was honestly expected.",
    "GUILTY on vibes, acquitted on technicalities.",
    "NOT GUILTY. Prosecution ki aura ko further investigation chahiye.",
    "GUILTY. Defendant ko apne last 17 messages reflect karne honge.",
    "Case closed because the evidence started yapping too much.",
    "GUILTY. Court ne kaha: confidence rakho, par map bhi dekh lo.",
    "NOT GUILTY, but the group chat remains unconvinced.",
    "GUILTY. Defendant ki planning ko beta testing mein bheja jayega.",
    "Judge declares a draw; dono ki logic equally buffering thi.",
    "GUILTY of unnecessary kalesh, pardoned for entertainment value.",
    "NOT GUILTY. Court officially blames the Wi-Fi.",
    "GUILTY. Appeal allowed only after grass has been touched.",
)

PUNISHMENTS = (
    "10 minute grass touch karni padegi.",
    "group chat ko ek sincere 'my bad bhai' bhejna padega.",
    "apni aura ko reboot karke wapas aana padega.",
    "next message bina 'bro' ke likhna padega.",
    "ek snack court fee ke roop mein imaginary jama karna padega.",
    "five minutes ke liye NPC mode mein rehna padega.",
    "Google Maps se apni life direction verify karni padegi.",
    "apne braincells ki emergency meeting bulani padegi.",
    "ek wholesome compliment dena padega, bina sarcasm ke.",
    "loading screen ko patiently respect karna padega.",
    "apni planning sheet mein pehla actual step likhna padega.",
    "server ke sabse quiet member ko 'aap sahi keh rahe ho' bolna padega.",
    "10 minute tak sirf facts, no vibes allowed.",
    "ek apology draft karna padega aur is baar send bhi karna padega.",
    "apne latest hot take ko patch notes ke saath submit karna padega.",
    "ek imaginary traffic cone ko life advice deni padegi.",
    "next debate mein dramatic background music ke bina survive karna padega.",
    "apne notification panel ko dekhkar accountability accept karni padegi.",
    "ek round ke liye group chat ka side character banna padega.",
    "court ke order par hydration aur grass dono mandatory hain.",
)


class Kalesh(commands.Cog):
    """The isolated fictional courtroom feature."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kalesh", description="Create a harmless fictional courtroom case.")
    @app_commands.describe(user1="The plaintiff", user2="The defendant")
    async def kalesh(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member) -> None:
        bot_user = self.bot.user
        if bot_user and (user1.id == bot_user.id or user2.id == bot_user.id):
            await interaction.response.send_message(
                embed=embed(
                    "⚖️ KALESH COURT",
                    "Bot ko witness box mein bulaya ja sakta hai, par bot ko prosecute nahi kiya ja sakta. "
                    "Court ne dono parties ko snacks ke saath ghar bhej diya.",
                    "purple",
                ),
                ephemeral=True,
            )
            return

        if user1.id == user2.id:
            await interaction.response.send_message(
                embed=embed(
                    "⚖️ KALESH COURT",
                    f"**{member_name(user1)}** khud ke against case nahi chala sakta.\n\n"
                    "Plaintiff aur defendant same nikle. Court ne isse advanced self-kalesh declare karke "
                    "hearing adjourn kar di.",
                    "gold",
                ),
                ephemeral=True,
            )
            return

        case = embed("⚖️ KALESH COURT", "Justice is temporary. Kalesh is forever.", "gold")
        case.add_field(name="📜 Case Title", value=random.choice(CASE_TITLES), inline=False)
        case.add_field(name="👤 Plaintiff", value=member_name(user1), inline=True)
        case.add_field(name="👤 Defendant", value=member_name(user2), inline=True)
        case.add_field(name="🚨 Ilzaam / Accusation", value=random.choice(ACCUSATIONS), inline=False)
        case.add_field(name="🕵️ Fake Evidence", value=random.choice(EVIDENCE), inline=False)
        case.add_field(name="🗣️ Prosecution", value=random.choice(PROSECUTION), inline=False)
        case.add_field(name="🛡️ Defense", value=random.choice(DEFENSE), inline=False)
        case.add_field(name="⚖️ Judge's Verdict", value=random.choice(VERDICTS), inline=False)
        case.add_field(name="💀 Funny Punishment", value=random.choice(PUNISHMENTS), inline=False)
        case.set_footer(text="Justice is temporary. Kalesh is forever.")
        await interaction.response.send_message(embed=case)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Kalesh(bot))