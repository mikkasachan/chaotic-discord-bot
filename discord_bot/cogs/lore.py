from __future__ import annotations

import random

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import embed, member_name


ARCHETYPES = (
    "Professional NPC pretending to be the main character.",
    "Sleep-deprived lore goblin with premium side-quest energy.",
    "Accidental strategist operating on pure vibes.",
    "Group-chat historian who remembers the wrong details.",
    "Chaotic neutral snack philosopher.",
    "Loading-screen hero with a surprisingly dramatic soundtrack.",
    "Certified yapper with occasional wisdom DLC.",
    "Part-time villain, full-time reaction-image curator.",
    "Mysterious side character who knows too much.",
    "Aura merchant with an unstable inventory.",
    "Unlicensed server detective.",
    "Main-character intern on a probation arc.",
    "Brainrot scholar from the forbidden algorithm.",
    "Friendly final boss with questionable tactics.",
    "Human notification that refuses to be cleared.",
    "Overthinking wizard with zero spell cooldowns.",
    "Wi-Fi-powered chaos monk.",
    "Professional 'bro trust me' consultant.",
    "Plot-twist enthusiast with no outline.",
    "Low-battery legend running on emergency charisma.",
    "Certified grass-avoidance specialist.",
    "Side-quest speedrunner who forgets the main quest.",
    "Unofficial server weather reporter.",
    "NPC dialogue designer with one voice line.",
    "Vibes-based life coach.",
    "Suspiciously confident tutorial character.",
    "Snack-powered diplomatic envoy.",
    "Human typo with excellent timing.",
    "Lore librarian who keeps misplacing the canon.",
    "Chaos intern awaiting full-time employment.",
)

ORIGINS = (
    "Legend ke according, ye banda 3 AM pe server join hua tha aur tab se properly logout nahi hua.",
    "Iski origin story ek missing charger aur teen unanswered calls se start hoti hai.",
    "Kaha jaata hai ki isne ek baar vending machine ko debate mein hara diya tha.",
    "Ye server mein accidentally aaya tha, phir algorithm ne ise permanent resident bana diya.",
    "Iska pehla tutorial ek group chat tha jahan kisi ko bhi context nahi mila.",
    "Bachpan mein isne remote ka last working battery dhoondh kar destiny unlock ki.",
    "Iski pehli legendary achievement thi: bina map ke kitchen tak pahunchna.",
    "Ye ek aise timeline se aaya hai jahan 'seen' ek formal legal response hai.",
    "Origin ke din iske paas zero aura tha, par confidence unlimited trial par tha.",
    "Ek suspicious meme ne iske andar ke main character ko jagaya.",
    "Isne pehli baar lore tab banaya jab kisi ne poocha, 'tu online kyun hai?'",
    "Iski journey ek typo se shuru hui jo ab server canon ban chuka hai.",
    "Kehte hain isne school ke last bench se stealth mechanics seekhe.",
    "Iska janam ek unfinished side quest ke beech hua, objective abhi bhi unknown hai.",
    "Ek baar isne calendar ko ignore kiya aur tab se dates ise trust nahi karti.",
    "Isne Wi-Fi password yaad karke apni pehli magical ability unlock ki.",
    "Origin story mein ek raincoat, ek snack aur bahut zyada overconfidence hai.",
    "Ye pehle sirf lurk karta tha; phir ek reaction emoji ne ise bolne par majboor kiya.",
    "Isne ek harmless debate ko trilogy bana kar cinematic universe start kiya.",
    "Iski first boss fight ek stuck jar thi. Result confidential hai.",
    "Legend bolti hai isne ek baar notification ko ignore karke time travel kar liya.",
    "Ye server mein ek normal user banke aaya tha; normal part 11 minutes chala.",
    "Iska first power-up 'bro explain' sunte hi activate hua.",
    "Iski destiny ek half-written bio aur full-volume playlist ne decide ki.",
    "Isne ek baar wrong chat mein perfect message bheja aur tab se reality suspicious hai.",
    "Origin ke time iske braincells ne group project kiya, leader aaj tak missing hai.",
    "Kisi forgotten poll mein isne 'maybe' vote kiya tha; uske consequences legendary hain.",
    "Iski backstory mein ek bus miss, ek snack win aur ek dramatic comeback hai.",
    "Ye ek loading screen ko patiently dekhte-dekhte patience ka final form ban gaya.",
    "Isne apni pehli aura ek mirror selfie nahi, ek perfectly timed reaction se earn ki.",
    "Ek random Tuesday ko isne decide kiya ki ordinary rehna optional hai.",
    "Kehte hain iske first words the: 'guys suno, ek idea hai'.",
    "Iski lore ek lost sock ke investigation se unexpectedly expand hui.",
    "Isne ek boring meeting mein imaginary boss battle imagine karke survival seekha.",
    "Origin document ka pehla page blank hai, kyunki author bhi confused tha.",
    "Ye ek meme ke comment section se nikla aur server tak speedran karke aaya.",
    "Isne ek baar alarm ko snooze karke alternate universe ka internship le liya.",
    "Iski legacy ka first chapter ek dramatic exit aur instant rejoin se likha gaya.",
    "Isne ek broken pen ko sword samajhkar imagination ka skill tree unlock kiya.",
    "Origin story ke witnesses kehte hain: 'vibes weird thi, par entertaining bhi'.",
)

ABILITIES = (
    "5 seconds mein conversation ko completely off-topic kar dena.",
    "Bina context ke bhi full confidence se explanation dena.",
    "Ek notification ko dekhkar reply ka trailer release karna.",
    "Har situation mein snack ka hidden solution dhoondhna.",
    "Wrong answer ko itne confidence se bolna ki room doubt karne lage.",
    "3 AM par sudden philosophical wisdom unlock karna.",
    "Ek emoji se poora emotional paragraph communicate karna.",
    "Loading screen ko dekhkar bhi somehow late hona.",
    "Group chat mein dead conversation ko accidental chaos se revive karna.",
    "Apni galti ko limited-edition plot twist bana dena.",
    "Har plan mein secret side quest add karna.",
    "Dusron ke braincells ko temporary loan par lena.",
    "Aise disappear hona jaise Wi-Fi ne personally dhokha diya ho.",
    "Ek simple question ka cinematic universe banana.",
    "Randomly perfect timing par funniest line bolna.",
    "Bina preparation ke courtroom-level defense dena.",
    "Kisi bhi silence ko 'kalesh incoming' mein convert karna.",
    "Typing indicator se suspense thriller create karna.",
    "Apni aura ko low battery par bhi online rakhna.",
    "Har meme mein apni autobiography dekh lena.",
    "Ek hi story ke chaar director's cuts banana.",
    "Wrong route ko scenic route declare karna.",
    "Conversation ko wholesome se unhinged mode mein switch karna.",
    "Kisi bhi boring task ko dramatic mission banana.",
    "Instantly detect karna ki kis message mein suspicious vibes hain.",
    "Brainrot ko fluent second language ki tarah use karna.",
    "Group project mein last minute miracle summon karna.",
    "Awkward moment ko joke se successfully escape karna.",
    "Ek reaction se poori server politics change kar dena.",
    "Silently observe karke exact moment par critical hit dialogue dena.",
)

WEAKNESSES = (
    "Ek simple 'bro explain' aur pura system crash.",
    "Low battery dekhte hi saari strategic thinking vanish.",
    "Do options milte hi third option invent karna.",
    "Apna charger kisi safe jagah rakhkar us safe jagah ko bhool jaana.",
    "Koi 'urgent' likh de toh instantly overthink mode activate.",
    "Tutorial skip karne ke baad tutorial ki zaroorat padna.",
    "Apology type karna, send button se emotional distance rakhna.",
    "Ek notification ke baad poora focus side quest par chala jaana.",
    "Calendar ke saath trust issues.",
    "Simple instructions ko optional lore samajhna.",
    "Pehle answer dena, phir question padhna.",
    "Grass ka naam sunte hi internet par wapas teleport hona.",
    "Aise jokes jo sirf isse funny lagte hain.",
    "Group chat ka 'we need to talk' message.",
    "Apni hi planning sheet ka first step.",
    "Koi bina context ke 'interesting' bol de.",
    "Password yaad hota hai, username nahi.",
    "Achanak saamne aa jaata hua accountability.",
    "Do minute ka kaam jo calendar event ban jaaye.",
    "Jab Wi-Fi full bars dikhakar bhi kaam na kare.",
    "Apni voice note ko send karne se pehle dobara sunna.",
    "Ek hi waqt par do log reply kar dein.",
    "Kisi ka 'calm down' kehna.",
    "Braincells ka attendance check.",
    "Public mein apna typo discover karna.",
    "Aisa meme jiska context samajh na aaye.",
    "Alarm jo actually follow-up maange.",
    "Koi iski lore ko fact-check karne lage.",
    "Apni overconfidence ka screenshot.",
    "Jab side quest accidentally main quest ban jaaye.",
)

ARCS = (
    "Currently aura grind kar raha hai, par accidentally aura lose bhi kar raha hai.",
    "Main character banne nikla tha, ab side quest ka CEO hai.",
    "Braincells ko reorganize karne ka arc chal raha hai; results pending.",
    "Currently 'reply later' se 'reply never' tak ka speedrun kar raha hai.",
    "Skill issue ko skill tree mein convert karne ki koshish jaari hai.",
    "Server mein wholesome rehne ka experiment day two par fail ho gaya.",
    "Apne NPC dialogue ko upgrade karke premium yapper ban raha hai.",
    "Loading screen se bahar aane ka arc technically start ho chuka hai.",
    "Grass touch karne ka plan bana hai; execution committee missing hai.",
    "Currently ek snack aur ek dramatic comeback ke beech phansa hua hai.",
    "Apni planning ko beta version se stable release banane ki journey mein hai.",
    "Vibes ko organize kar raha hai, folders abhi empty hain.",
    "Ek normal Tuesday ko legendary banane ki suspicious koshish chal rahi hai.",
    "Overthinking ko productivity bolne wale arc ka final episode aa raha hai.",
    "Abhi apni aura ka software update install kar raha hai.",
    "Group chat mein silent observer se occasional final boss ban chuka hai.",
    "Current arc: confidence high, map usage critically low.",
    "Apne inner side character ko main story ka contract dilwa raha hai.",
    "Plot twist se bachne gaya tha, khud plot twist ban gaya.",
    "Abhi 'bro trust me' ko actual evidence se replace karne ki training mein hai.",
    "Chaos ko monetize nahi, bas responsibly deploy karne ka phase hai.",
    "Life ke tutorial ko skip karke walkthrough comments padh raha hai.",
    "Apni late replies ko historical archive declare karne ka arc.",
    "Current mission: braincells ko ek hi meeting mein laana.",
    "Server ke lore mein cameo se recurring character banne ki race mein hai.",
    "Aajkal har decision ko director's cut mil raha hai.",
    "Apni vibe ko mysterious samajhta hai, algorithm ise confused bolta hai.",
    "Currently confidence ko skills ke saath sync karne ki koshish.",
    "Ek harmless idea ko overpowered saga banane ka arc active hai.",
    "Canon update pending; personality patch notes surprisingly long hain.",
)

PREDICTIONS = (
    "Ek din server ka most wanted NPC banega.",
    "Future mein iska aura meter positive number dekh sakta hai.",
    "Kisi random Tuesday ko perfect comeback time par unlock hoga.",
    "Iska next side quest accidentally server event banega.",
    "Braincells ki emergency meeting finally quorum achieve karegi.",
    "Ek snack iski destiny ka major plot point banega.",
    "Aane wale arc mein ye grass ko kam se kam screenshot mein dekhega.",
    "Iski next big achievement ek message ko same day reply karna hogi.",
    "Algorithm ise mysterious nahi, iconic category mein daalne wala hai.",
    "Kisi debate mein iski logic aur vibes pehli baar alliance banayengi.",
    "Ek din ye bina 'bro' bole poora sentence complete karega.",
    "Iski lore ka next chapter ek suspiciously good idea se start hoga.",
    "Future mein iska NPC dialogue limited edition collectible banega.",
    "Ek random compliment iski aura ko critical hit dega.",
    "Iska next comeback late hoga, par surprisingly worth the wait.",
    "Server ki history mein iska naam footnote nahi, chaotic heading banega.",
    "Kabhi na kabhi ye apni planning sheet ka second step bhi likhega.",
    "Aane wale season mein side quest main quest ko temporarily replace karega.",
    "Iske braincells ek din group project successfully submit karenge.",
    "Ek din Wi-Fi isse bina drama ke connect ho jayega.",
    "Iski future arc mein accountability ka cameo confirmed hai.",
    "Kisi future poll mein iski choice unexpectedly correct niklegi.",
    "Ye ek harmless kalesh ko wholesome resolution tak le jayega.",
    "Aane wale dinon mein iska confidence aur skills 720p par milenge.",
    "Ek perfect reaction emoji iski reputation save karega.",
    "Future mein iski timing itni accurate hogi ki memes jealous honge.",
    "Iska next lore drop server ke canon ko aur questionable karega.",
    "Ek din ye loading screen ko blame kiye bina wait karega.",
    "Iski aura ka next update undocumented but powerful hoga.",
    "Eventually, ye apni own side quest ka final boss defeat karega.",
)


class Lore(commands.Cog):
    """Persistent, fictional Member Lore generation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="lore", description="Generate evolving fictional lore for a member.")
    @app_commands.describe(user="Whose fictional lore should become dangerously specific?")
    async def lore(self, interaction: discord.Interaction, user: discord.Member) -> None:
        bot_user = self.bot.user
        if bot_user and user.id == bot_user.id:
            case = embed("📖 LORE DATABASE // ChaosBot", "The bot's lore is classified by three servers and one suspicious pigeon.", "purple")
            case.add_field(name="⭐ Lore Level", value="`∞ (probably)`", inline=True)
            case.add_field(name="🎭 Archetype", value="Wi-Fi-powered dungeon master with no off switch.", inline=True)
            case.add_field(name="📜 Origin Story", value="Born from a terminal window and an unreasonable amount of server energy.", inline=False)
            case.add_field(name="🧠 Special Ability", value="Turning one slash command into a full cinematic universe.", inline=False)
            case.add_field(name="💀 Biggest Weakness", value="A missing environment variable and overly confident error messages.", inline=False)
            case.add_field(name="🔥 Current Arc", value="Pretending the logs are under control.", inline=False)
            case.add_field(name="🔮 Future Prediction", value="Will eventually ask everyone to touch grass, politely.", inline=False)
            case.set_footer(text="Canon status: questionable.")
            await interaction.response.send_message(embed=case)
            return

        if not interaction.guild:
            await interaction.response.send_message(
                embed("📖 MEMBER LORE", "Lore ko server audience chahiye. DMs mein canon ka budget nahi hai.", "purple"),
                ephemeral=True,
            )
            return

        stats = self.bot.db.record_lore(interaction.guild.id, user.id)
        level = stats["lore_level"]
        case = embed(f"📖 LORE DATABASE // {member_name(user)}", "Fictional canon only. Reality has been muted.", "purple")
        case.add_field(name="👤 Character", value=member_name(user), inline=False)
        case.add_field(name="⭐ Lore Level", value=f"`{level}/100`", inline=True)
        case.add_field(name="🎭 Archetype", value=random.choice(ARCHETYPES), inline=True)
        case.add_field(name="📜 Origin Story", value=random.choice(ORIGINS), inline=False)
        case.add_field(name="🧠 Special Ability", value=random.choice(ABILITIES), inline=False)
        case.add_field(name="💀 Biggest Weakness", value=random.choice(WEAKNESSES), inline=False)
        case.add_field(name="🔥 Current Arc", value=random.choice(ARCS), inline=False)
        case.add_field(name="🔮 Future Prediction", value=random.choice(PREDICTIONS), inline=False)
        case.set_footer(text=f"Canon status: questionable. Lore drops: {stats['lore_count']}")
        await interaction.response.send_message(embed=case)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Lore(bot))