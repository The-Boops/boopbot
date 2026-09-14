import discord
import random
import logging
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('boopbot.log')
    ]
)
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('discord.http').setLevel(logging.ERROR)
logging.getLogger('discord.gateway').setLevel(logging.ERROR)
logging.getLogger('discord.client').setLevel(logging.ERROR)

logger = logging.getLogger('boopbot')

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    async def on_ready(self):
        guild = discord.Object(id=1484668539976814725)
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)
        await client.change_presence(activity=discord.CustomActivity(name="if offline: maintenance, updates, or host issues"))
        logger.info(f'Logged in as {self.user.name}')

client = MyClient(intents=intents)
tree = discord.app_commands.CommandTree(client)

EIGHTBALL_RESPONSES = [
    'Yes.', 'No.', 'Maybe.', 'Definitely.', 'Absolutely not.', 'Ask again later.', 'Without a doubt.', 'Very doubtful.', 'It is certain.', 'Cannot predict now.', 'Most likely.', 'Outlook not so good.', 'Yes, in due time.', 'My sources say no.', 'You may rely on it.', 'Better not tell you now.', 'Concentrate and ask again.', 'Signs point to yes.', 'Reply hazy, try again.', "Don't count on it.", 'Yes, you can do it!', 'No way!', 'The answer is unclear.', 'Yes, but be cautious.', 'Absolutely!', 'I have my doubts.', 'Yes, but it will take time.', 'No, but keep trying.', 'Yes, and you will succeed.', "No, but don't give up!", 'Yes, and good things are coming your way.', 'No, but stay positive!', 'Yes, and you will achieve your goals.', 'No, but keep learning and growing.', 'Yes, and you will find happiness.', 'No, but stay hopeful!', 'Yes, and you will overcome challenges.', 'No, but keep moving forward!', 'Yes, and you will find love.', 'No, but stay strong!', 'Yes, and you will find success.', 'No, but keep believing in yourself!', 'Yes, and you will find peace.', 'No, but stay determined!', 'Yes, and you will find joy.', 'No, but keep striving for greatness!', 'Yes, and you will find fulfillment.', 'No, but stay motivated!', 'Yes, and you will find purpose.', 'No, but keep pushing forward!', 'Yes, and you will find clarity.', 'No, but stay focused!', 'Yes, and you will find balance.', 'No, but keep working hard!', 'Yes, and you will find inspiration.', 'No, but stay resilient!', 'Yes, and you will find strength.', 'No, but keep persevering!', 'Yes, absolutely!', 'Of course!', 'Without question!', '100% yes!', 'Yes, and you got this!', 'Undeniably yes.', 'The stars say yes.', 'Yes, trust yourself.', 'Clearly yes.', 'Yes, no doubt about it.', 'The universe says yes.', 'Yes, believe it!', 'Affirmative!', 'Yes, and it will be great.', 'Positively yes!'
]

@tree.command(name="roll", description="Roll a die")
async def roll(interaction: discord.Interaction, sides: int = 6):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /roll sides={sides}')
    result = random.randint(1, sides)
    await interaction.response.send_message(f'🎲 You rolled a {result} (d{sides})')

@tree.command(name="8ball", description="Ask the magic 8 ball")
async def eightball(interaction: discord.Interaction, question: str):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /8ball: {question}')
    await interaction.response.send_message(f'🎱 {random.choice(EIGHTBALL_RESPONSES)}')

@tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /coinflip')
    result = random.choice(['Heads! 🪙', 'Tails! 🪙'])
    await interaction.response.send_message(result)

@tree.command(name="choose", description="Pick from options")
async def choose(interaction: discord.Interaction, options: str):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /choose: {options}')
    choices = [o.strip() for o in options.split('|') if o.strip()]
    if not choices:
        await interaction.response.send_message('❌ Provide options separated by | e.g. `pizza | burger | tacos`')
    else:
        await interaction.response.send_message(f'🎯 I choose: **{random.choice(choices)}**')

@tree.command(name="random", description="Random number, joke, fact or advice")
async def random_cmd(interaction: discord.Interaction, type: str, low: int = 1, high: int = 100):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /random type={type}')
    if type == 'number':
        await interaction.response.send_message(f'Your random number is: {random.randint(low, high)}')
    elif type == 'joke':
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why did the bicycle fall over? Because it was two-tired!",
            "Why did the math book look sad? Because it had too many problems.",
            "Why did the tomato turn red? Because it saw the salad dressing!"
        ]
        await interaction.response.send_message(random.choice(jokes))
    elif type == 'fact':
        facts = [
            "Honey never spoils. Archaeologists have found 3,000 year old honey in Egyptian tombs.",
            "Bananas are berries, but strawberries are not.",
            "A day on Venus is longer than a year on Venus.",
            "Octopuses have three hearts and blue blood.",
            "There are more stars in the universe than grains of sand on all beaches on Earth."
        ]
        await interaction.response.send_message(random.choice(facts))
    elif type == 'advice':
        advices = [
            "Don't be afraid to ask for help when you need it.",
            "Take breaks and give yourself time to recharge.",
            "Stay positive and focus on the good things in life.",
            "Learn from your mistakes and keep moving forward.",
            "Be kind to yourself and others."
        ]
        await interaction.response.send_message(random.choice(advices))
    else:
        await interaction.response.send_message('❌ Type must be: number, joke, fact, or advice')

@tree.command(name="userinfo", description="Get info about a user")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /userinfo on {target.display_name}')
    is_bot = 'Yes' if target.bot else 'No'
    await interaction.response.send_message(
        f'**User Info:**\n'
        f'Name: {target.display_name}\n'
        f'ID: {target.id}\n'
        f'Bot: {is_bot}'
    )

@tree.command(name="help", description="List all commands")
async def help_cmd(interaction: discord.Interaction):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /help')
    await interaction.response.send_message(
        '**Commands:**\n'
        '`gm` / `gn` / `hello` / `bye` - Greetings\n'
        '`ping` / `pong` / `boop` - Fun responses\n'
        '`/roll [sides]` - Roll a die\n'
        '`/8ball <question>` - Magic 8 ball\n'
        '`/random <type>` - number/joke/fact/advice\n'
        '`/coinflip` - Heads or tails\n'
        '`/choose <a | b | c>` - Pick an option\n'
        '`/userinfo [@user]` - User info\n'
        '`/help` - This message'
    )

@tree.command(name="boop", description="Boop!")
async def boop(interaction: discord.Interaction):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /boop')
    await interaction.response.send_message(f'Boop!')

@tree.command(name="ping", description="Pong!")
async def ping(interaction: discord.Interaction):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /ping')
    await interaction.response.send_message(f'Pong! {interaction.user.display_name}!')

@tree.command(name="gm", description="Good morning!")
async def gm(interaction: discord.Interaction):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /gm')
    await interaction.response.send_message(f'gm {interaction.user.display_name}!')

@tree.command(name="gn", description="Good night!")
async def gn(interaction: discord.Interaction):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /gn')
    await interaction.response.send_message(f'gn {interaction.user.display_name}!')

@tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    logger.info(f'{interaction.user.display_name} ({interaction.user.id}) used /hello')
    await interaction.response.send_message(f'Hello {interaction.user.display_name}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    raw = message.content.strip()
    
    # ! commands work without trigger
    if not raw.startswith('!'):
        bot_mention = f'<@{client.user.id}>'
        has_trigger = raw.endswith('BoopBot') or raw.endswith(bot_mention)
        if not has_trigger:
            return
        for trigger in ['BoopBot', bot_mention]:
            if raw.endswith(trigger):
                raw = raw[:-len(trigger)].strip()
                break
    
    content = raw.lower()

    if content == 'gm':
        logger.info(f'{message.author.display_name} ({message.author.id}) said gm')
        await message.channel.send(f'gm {message.author.display_name}!')
    elif content == 'gn':
        logger.info(f'{message.author.display_name} ({message.author.id}) said gn')
        await message.channel.send(f'gn {message.author.display_name}!')
    elif content == 'hello':
        logger.info(f'{message.author.display_name} ({message.author.id}) said hello')
        await message.channel.send(f'Hello {message.author.display_name}!')
    elif content == 'bye':
        logger.info(f'{message.author.display_name} ({message.author.id}) said bye')
        await message.channel.send(f'Bye {message.author.display_name}!')
    elif content == 'how are you?':
        logger.info(f'{message.author.display_name} ({message.author.id}) asked how are you')
        await message.channel.send(f"I'm good, {message.author.display_name}! How about you?")
    elif content == 'i am good':
        logger.info(f'{message.author.display_name} ({message.author.id}) said i am good')
        await message.channel.send(f"That's great to hear, {message.author.display_name}!")
    elif content == 'i am not good':
        logger.info(f'{message.author.display_name} ({message.author.id}) said i am not good')
        await message.channel.send(f"I'm sorry to hear that, {message.author.display_name}. I hope things get better for you soon.")
    elif content == 'boop':
        logger.info(f'{message.author.display_name} ({message.author.id}) said boop')
        await message.channel.send(f'Boop!')
    elif content == 'ping':
        logger.info(f'{message.author.display_name} ({message.author.id}) said ping')
        await message.channel.send(f'Pong! {message.author.display_name}!')
    elif content == 'pong':
        logger.info(f'{message.author.display_name} ({message.author.id}) said pong')
        await message.channel.send(f'Ping! {message.author.display_name}!')
    elif content.startswith('!random number'):
        parts = content.split()
        low, high = 1, 100
        if len(parts) == 4 and parts[2].isdigit() and parts[3].isdigit():
            low, high = int(parts[2]), int(parts[3])
        if low >= high:
            await message.channel.send('❌ First number must be less than second!')
        else:
            logger.info(f'{message.author.display_name} ({message.author.id}) used !random number {low} {high}')
            number = random.randint(low, high)
            await message.channel.send(f'Your random number is: {number}')
    elif content == '!random joke':
        logger.info(f'{message.author.display_name} ({message.author.id}) used !random joke')
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why did the bicycle fall over? Because it was two-tired!",
            "Why did the math book look sad? Because it had too many problems.",
            "Why did the tomato turn red? Because it saw the salad dressing!"
        ]
        await message.channel.send(random.choice(jokes))
    elif content == '!random fact':
        logger.info(f'{message.author.display_name} ({message.author.id}) used !random fact')
        facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
            "Bananas are berries, but strawberries are not.",
            "A day on Venus is longer than a year on Venus.",
            "Octopuses have three hearts and blue blood.",
            "There are more stars in the universe than grains of sand on all the beaches on Earth."
        ]
        await message.channel.send(random.choice(facts))
    elif content == '!random advice':
        logger.info(f'{message.author.display_name} ({message.author.id}) used !random advice')
        advices = [
            "Don't be afraid to ask for help when you need it.",
            "Take breaks and give yourself time to recharge.",
            "Stay positive and focus on the good things in life.",
            "Learn from your mistakes and keep moving forward.",
            "Be kind to yourself and others."
        ]
        await message.channel.send(random.choice(advices))
    elif content.startswith('!roll'):
        sides = 6
        parts = content.split()
        if len(parts) > 1 and parts[1].isdigit():
            sides = int(parts[1])
        logger.info(f'{message.author.display_name} ({message.author.id}) used !roll d{sides}')
        result = random.randint(1, sides)
        await message.channel.send(f'🎲 You rolled a {result} (d{sides})')
    elif content.startswith('!8ball'):
        question = message.content[7:].strip()
        if not question:
            await message.channel.send('🎱 Ask a question! e.g. `!8ball will I pass my exam?`')
        else:
            logger.info(f'{message.author.display_name} ({message.author.id}) used !8ball: {question}')
            await message.channel.send(f'🎱 {random.choice(EIGHTBALL_RESPONSES)}')
    elif content == '!help':
        logger.info(f'{message.author.display_name} ({message.author.id}) used !help')
        await message.channel.send(
            '**Commands:**\n'
            '`gm` / `gn` / `hello` / `bye` - Greetings\n'
            '`ping` / `pong` - Ping pong\n'
            '`boop` - Boop!\n'
            '`!roll [sides]` - Roll a die\n'
            '`!8ball <question>` - Magic 8 ball\n'
            '`!random number [low] [high]` - Random number\n'
            '`!random joke` - Random joke\n'
            '`!random fact` - Random fact\n'
            '`!random advice` - Random advice\n'
            '`!coinflip` - Heads or tails\n'
            '`!choose a | b | c` - Pick an option\n'
            '`!userinfo` - Your user info'
        )
    elif content == '!coinflip':
        logger.info(f'{message.author.display_name} ({message.author.id}) used !coinflip')
        result = random.choice(['Heads! 🪙', 'Tails! 🪙'])
        await message.channel.send(result)
    elif content.startswith('!choose'):
        options = message.content[8:].strip().split('|')
        options = [o.strip() for o in options if o.strip()]
        if not options:
            await message.channel.send('❌ Provide options! e.g. `!choose pizza | burger | tacos`')
        else:
            logger.info(f'{message.author.display_name} ({message.author.id}) used !choose: {options}')
            await message.channel.send(f'🎯 I choose: **{random.choice(options)}**')
    elif content.startswith('!userinfo'):
        mentions = message.mentions
        if mentions:
            target = mentions[0]
        else:
            target = message.author
        logger.info(f'{message.author.display_name} ({message.author.id}) used !userinfo on {target.display_name}')
        is_bot = 'Yes' if target.bot else 'No'
        await message.channel.send(
            f'**User Info:**\n'
            f'Name: {target.display_name}\n'
            f'ID: {target.id}\n'
            f'Bot: {is_bot}'
        )

client.run(os.getenv('DISCORD_BOT_TOKEN'))