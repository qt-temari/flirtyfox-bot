import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import logging

TOKEN = os.environ.get("BOT_TOKEN")  # Replace with your actual bot token

# LOGGING SETUP
logging.basicConfig(level=logging.INFO)

# UTIL FUNCTION
async def send_typing_then_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str, reply_to_message_id=None):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_html(
        text=message,
        reply_to_message_id=reply_to_message_id
    )

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    welcome_msg = (
        f"🌟 Welcome {user.mention_html()} to Flirty Fox! 🌟\n\n"
        "Get ready for a journey filled with fun, laughter, and a touch of spice! 🔥\n\n"
        "✨ Available Commands: ✨\n"
        "💖 /love - Check love percentage\n"
        "🥵 /horny - Check your horny level\n"
        "🤤 /pervy - Check your pervy level\n"
        "🔥 /sexrate - Rate your sex power\n"
        "💌 /facts - Romantic or sexual facts\n"
        "💥 /roast - Roast someone with a zing!\n"
        "💘 /flirt - Get a flirty line for the day\n"
        "💡 /tips - Romantic & sexual tips\n"
        "❓ /t - Truth question\n"
        "🎲 /d - Dare challenge\n"
        "👋 /slap - Get a playful slap reply\n\n"
        "Let the adventure begin! ✋😝🤚"
    )

    keyboard = [
        [
            InlineKeyboardButton("Updates", url="https://t.me/WorkGlows"),
            InlineKeyboardButton("Support", url="https://t.me/TheCryptoElders"),
        ],
        [
            InlineKeyboardButton("Repository", url="https://github.com/asadofc/flirtfox-bot"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_html(
        text=welcome_msg,
        reply_markup=reply_markup
    )

# RANDOM %
async def handle_random_percent(update: Update, context: ContextTypes.DEFAULT_TYPE, label: str):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        name = user.mention_html()
        reply_to = update.message.reply_to_message.message_id
    elif context.args:
        name = " ".join(context.args)
        reply_to = None
    else:
        await send_typing_then_reply(update, context, f"Please provide a name or reply to someone!")
        return

    percent = random.randint(10, 100)
    if percent <= 20:
        feedback = "Not impressive... Needs some work!"
    elif percent <= 40:
        feedback = "Hmm, you're getting there!"
    elif percent <= 60:
        feedback = "Decent! You've got potential."
    elif percent <= 80:
        feedback = "Ooh, quite spicy! Keep it up!"
    else:
        feedback = "You're an absolute legend at this!"

    await send_typing_then_reply(update, context, f"{name}, your {label} level is {percent}%\n\n{feedback}", reply_to_message_id=reply_to)

async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "love")

async def horny(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "horny")

async def pervy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "pervy")

async def sexrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "sex")

# LISTS
facts_list = [
    "❤️ Kissing can burn up to 6 calories a minute!",
    "💤 Cuddling helps release oxytocin, making you sleep better.",
    "✨ Eye contact for 2 minutes can make strangers fall in love.",
    "⚡ Orgasms relieve pain by releasing endorphins.",
    "❄️ Kissing boosts your immune system!",
    "❤️‍🔥 Morning sex boosts your mood for the whole day.",
    "❤️ Physical affection leads to lower blood pressure.",
    "🔥 Sexual activity improves heart health.",
    "🥰 Couples who laugh together stay together longer.",
    "❣️ 60 seconds of hugging releases oxytocin!",
    "❤️ Sex can actually count as light exercise!",
    "✨ Compliments trigger dopamine — the pleasure chemical.",
    "❤️‍🔥 People who flirt live longer, study says!",
    "🧠 Thinking about someone you love can decrease stress levels.",
    "🔥 Touching skin-to-skin calms your nervous system.",
    "❤️ Cuddling after intimacy strengthens bonds.",
    "❄️ Passionate kissing increases saliva flow — great for teeth!",
    "✨ Sexually satisfied people tend to perform better at work.",
    "❤️ Being in love lowers cortisol (stress hormone).",
    "❤️ Kissing can strengthen your relationship by improving communication.",
    "✨ Intimacy can strengthen your immune system over time.",
    "❤️ Foreplay can enhance emotional connection drastically.",
    "❤️ Oxytocin (love hormone) makes people more trusting.",
    "❤️ Touch triggers the brain’s reward center.",
    "✨ Even playful flirting releases feel-good hormones!",
    "❤️ Spontaneous romance keeps the relationship exciting.",
    "⚡ Partners who share adventures have stronger intimacy.",
    "❤️ Emotional intimacy often enhances physical intimacy.",
    "❤️ Smelling your partner’s scent can ease anxiety.",
    "✨ Sexual satisfaction correlates with overall happiness.",
    "❤️ Regular cuddles are linked to lower risk of depression.",
    "❣️ Holding hands literally synchronizes your heartbeat.",
    "❤️ Physical touch is a basic human need.",
    "✨ Sex burns between 100–300 calories per session!",
    "❤️ Making love can boost self-esteem and confidence.",
    "❤️ The brain reacts to love like it reacts to cocaine!",
    "✨ Flirting helps release serotonin — your happy chemical.",
    "❤️ Orgasms increase pain tolerance by up to 70%.",
    "❄️ Kissing involves over 30 facial muscles — workout bonus!",
    "❤️ Being playful together boosts relationship satisfaction.",
    "✨ Fantasizing about your partner strengthens attraction.",
    "❤️ Good communication = better sex, proven scientifically.",
    "❤️ Trust improves physical connection between partners.",
    "❣️ Teasing your partner increases sexual tension positively.",
    "✨ Laughing together increases attraction.",
    "❤️ Smiling during intimacy boosts connection deeply.",
    "⚡ Daily affirmations from partners build sexual confidence.",
    "❤️ Just thinking about someone you love relieves pain.",
    "✨ Sexual chemistry often starts in the mind.",
    "❤️ Long hugs (over 20 seconds) increase oxytocin.",
    "✨ Novelty in intimacy keeps passion alive longer.",
    "❤️ Playfulness outside the bedroom enhances passion inside it."
]

roast_list = [
    "😂 You’re like a cloud. When you disappear, it’s a beautiful day.",
    "😜 If I had a dollar for every smart thing you said, I’d be broke.",
    "🤣 You're the reason shampoo has instructions.",
    "😆 You bring everyone so much joy... when you leave the room.",
    "😝 You're the human version of a participation trophy.",
    "😏 You're slower than dial-up internet.",
    "😅 You're the 'before' picture in every advertisement.",
    "🙄 You’re proof that even evolution takes a break.",
    "😂 You're as useless as the 'g' in lasagna.",
    "😜 If awkward was an Olympic sport, you'd win gold.",
    "🤣 You’re like a cloud: when you vanish, it’s a beautiful day.",
    "😆 You have something on your chin... no, the third one down.",
    "😋 You’re the dictionary definition of 'meh'.",
    "😜 Your secrets are always safe with me. I never even listen when you tell me them.",
    "🙃 You're as sharp as a marble.",
    "😂 You could trip over a wireless internet connection.",
    "😝 I’d agree with you, but then we’d both be wrong.",
    "🤣 You're like a phone with no signal—nobody needs you.",
    "😆 Your brain is like a web browser: 19 tabs are open, but none of them are working.",
    "🥴 You look like a mistake, but at least you’re an original one.",
    "🤣 I’d explain it to you, but I left my English-to-Dingbat dictionary at home.",
    "😂 You're like a sandwich without filling—just plain and dry.",
    "😜 You have the perfect face for radio.",
    "😆 The only time you’ll be the center of attention is if you accidentally trip and fall.",
    "🤣 You're like a broken pencil—pointless.",
    "😅 You're the only person who can trip over a wireless connection.",
    "😏 You're not stupid; you just have bad luck thinking.",
    "😂 If I had a nickel for every time you said something smart, I'd be broke.",
    "😜 You're the reason the instructions on shampoo bottles exist.",
    "🤣 You're like a highlighter—bright, but ultimately unnecessary.",
    "😆 You have the perfect face for radio.",
    "🙃 If laziness was an Olympic sport, you’d be a gold medalist.",
    "😅 I'd agree with you, but then we’d both be wrong.",
    "🤣 If brains were taxed, you’d get a refund.",
    "😂 You make a rock look like a genius.",
    "😋 Your life is like a software update—just when you think it’s finished, there’s more.",
    "🤣 You’re like a math book—full of problems, no solutions.",
    "😂 You’re not stupid; you just have bad luck thinking.",
    "😜 You make a rock look like a genius.",
    "🙄 You're like a phone with no signal—nobody needs you.",
    "🥴 You can’t fix stupid, but you can put it on display.",
    "🤣 You're not stupid, you just have bad luck thinking.",
    "😏 If you were any more dense, you'd have your own gravitational pull.",
    "😂 If I had a penny for every dumb thing you said, I'd be rich by now.",
    "😝 I’m not saying you’re dumb, but you have a high chance of tripping over a cordless phone.",
    "😆 Your ideas are like unicorns—beautiful in theory but not real.",
    "🤣 You're like a broken clock—right twice a day, but still useless most of the time.",
    "😂 If stupidity was a crime, you’d be serving a life sentence.",
    "😜 I’ve seen salads dressed better than you.",
    "🤣 You're like a cloud—sometimes I think you’re floating away.",
    "😂 You can’t spell 'stupid' without 'u' and 'i'—wait, that doesn’t make sense.",
    "😋 You’d be a great example in a 'What Not To Do' documentary.",
    "🙄 Your head is so empty, it echoes when you talk.",
    "😆 You’re the kind of person who trips over a wireless connection.",
    "🤣 You have a face for radio and a voice for silent movies.",
    "😝 You're like a vending machine—people keep trying, but nobody wants to pay for you.",
    "😏 If I had a brain cell for every time you said something intelligent, I’d have zero.",
    "😂 You're the human version of a participation trophy.",
    "😜 You could be a superhero, but your superpower would be being invisible to intelligence.",
    "😆 The world needs more people like you... just not near me.",
    "🤣 You have the perfect face for radio and the perfect voice for silent movies.",
    "🙃 You're a few fries short of a Happy Meal.",
    "😂 You’re like a broken pencil—pointless.",
    "😝 Your Wi-Fi signal is stronger than your personality.",
    "😏 You’re like an IKEA bookshelf—confusing and nobody’s really sure how you’re supposed to fit in.",
    "🤣 If I had a nickel for every time you said something smart, I’d be broke.",
    "😆 You’re like a cloud—when you disappear, it’s a beautiful day.",
    "😝 If you were any more clueless, we’d need a map to find you.",
    "😏 If I had to rank your intelligence, I’d give you a solid 'meh'.",
    "🙄 You’re like a sloth with Wi-Fi—you move slow, but never get anything done.",
    "🤣 If I had a penny for every dumb thing you said, I’d have enough to buy you a brain.",
    "😂 You're the reason why instructions exist.",
    "😜 You're like a cookie without chocolate chips—plain and disappointing.",
    "😆 You're like a broken compass—lost without direction.",
    "🤣 You couldn’t pour water out of a boot if the instructions were on the heel.",
    "😏 You look like you’ve been hit by the stupid bus.",
    "😂 You're the reason they put warning labels on everything.",
    "😝 You’d be the best at staring contests... with yourself.",
    "🤣 If brains were taxed, you’d get a refund.",
    "😋 You're the reason they made instructions on shampoo bottles.",
    "🙄 You should come with a warning sign.",
    "😆 You're like a puzzle with a missing piece—just incomplete.",
    "🤣 You're like a lightbulb with no power—just sitting there.",
    "😜 If I had a brain, I’d tell you how dumb that was.",
    "😝 You’re the human version of a typo.",
    "😂 If you were any dumber, we’d need to put you in a museum.",
    "😋 Your mind is like a web browser—19 tabs open, but none are relevant.",
    "🤣 If you were any more lazy, you'd have to be double-parked.",
    "😂 You're the reason the phrase 'Good things come to those who wait' doesn't apply to you.",
    "🙄 You look like a 'before' picture in a weight loss ad.",
    "😝 You’re the type to give directions in a circle.",
    "😏 You could trip over flat ground.",
    "🤣 If there was a contest for stupidity, you’d win first place—no competition."
]

flirt_list = [
    "😍 Are you a magician? Because whenever I look at you, everyone else disappears.",
    "😉 You must be made of copper and tellurium, because you're Cu-Te.",
    "💖 Do you have a map? Because I keep getting lost in your eyes.",
    "🌹 If kisses were snowflakes, I’d send you a blizzard.",
    "😘 Are you French? Because Eiffel for you.",
    "💫 You must be a star, because your beauty lights up the whole room.",
    "💋 Is your name Google? Because you have everything I’ve been searching for.",
    "🌟 Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "❤️ Are you an angel? Because heaven is missing one.",
    "💘 I think you’re suffering from a lack of vitamin me.",
    "🔥 If beauty were a crime, you’d be serving a life sentence.",
    "✨ If I could rearrange the alphabet, I’d put U and I together.",
    "🌼 Your smile is the only sunshine I need.",
    "💖 I never believed in love at first sight, but that was before I saw you.",
    "😍 Is your name Wi-Fi? Because I’m feeling a connection.",
    "🌹 Are you a campfire? Because you’re hot and I want s’more.",
    "😘 Can I follow you home? Cause my parents always told me to follow my dreams.",
    "💘 Do you have a pencil? Because I want to erase your past and write our future.",
    "💫 If you were a vegetable, you’d be a cute-cumber.",
    "🔥 You must be a parking ticket, because you’ve got ‘fine’ written all over you.",
    "🌟 Your hand looks heavy, can I hold it for you?",
    "❤️ Do you have a mirror in your pocket? Because I can see myself in your pants.",
    "💋 Are you a time traveler? Because I see you in my future.",
    "🌼 I was blinded by your beauty... I’m going to need your name and number for insurance purposes.",
    "✨ If kisses were raindrops, I’d send you a storm.",
    "💖 Is your dad a boxer? Because you’re a knockout.",
    "💘 You’re so sweet, you’re giving me a toothache.",
    "🔥 If you were a vegetable, you’d be a cute-cumber.",
    "😍 I must be a snowflake, because I’ve fallen for you.",
    "🌹 Are you made of sugar? Because you’re sweet enough to give me a sugar rush.",
    "😘 If beauty were a crime, you’d be a life sentence.",
    "💫 Can you lend me a kiss? I promise I’ll give it back.",
    "🌟 Is it hot in here, or is it just you?",
    "💋 If I were a cat, I’d spend all 9 lives with you.",
    "❤️ Are you a photographer? Because I can picture us together.",
    "✨ You must be a magician, because whenever I look at you, everyone else disappears.",
    "😍 Are you from Paris? Because Eiffel for you.",
    "🌼 You had me at hello.",
    "💘 Are you a time traveler? Because I see you in my future.",
    "💖 I’m not a photographer, but I can picture us together.",
    "🔥 Are you a flame? Because you’re so hot, I can’t look away.",
    "🌹 I’m not a genie, but I can grant your wishes.",
    "💋 You must be a campfire, because you’re hot and I want s’more.",
    "💫 If you were a fruit, you’d be a fineapple.",
    "❤️ Do you have a pencil? Because I want to draw you a kiss.",
    "🌟 You must be tired because you’ve been running through my mind all day.",
    "😘 You must be the square root of negative one, because you can’t be real.",
    "💖 Are you a dictionary? Because you add meaning to my life.",
    "🌼 You brighten my day just by being you.",
    "💘 You’re so sweet, you make sugar jealous.",
    "😍 I must be a snowflake because I’ve fallen for you.",
    "🌹 Are you a bank loan? Because you have my interest.",
    "💋 Are you a star? Because your beauty lights up the night.",
    "💫 You make my heart race faster than the speed of light.",
    "❤️ Are you a cake? Because you’re as sweet as can be.",
    "💘 Are you an angel? Because heaven is missing one.",
    "🔥 You must be fire because you make me feel alive.",
    "🌼 I must be dreaming because you’re too perfect to be real.",
    "💖 Are you a wish? Because you just came true.",
    "🌟 You’re like a dictionary, you add meaning to my life.",
    "💋 Can I borrow a kiss? I promise I’ll give it back.",
    "✨ You must be the reason for global warming because you're too hot.",
    "😍 If you were a fruit, you'd be a fineapple.",
    "💘 Are you an alien? Because your beauty is out of this world.",
    "🌹 If you were a vegetable, you'd be a cute-cumber.",
    "💋 Are you made of chocolate? Because you’re sweet and irresistible.",
    "🔥 Are you a magnet? Because you’re attracting me.",
    "🌼 Your smile is my favorite part of the day.",
    "💖 I must be a snowflake, because I’ve fallen for you.",
    "💘 You make my heart race faster than a Ferrari.",
    "🌟 If kisses were snowflakes, I’d send you a blizzard.",
    "✨ Can you feel the sparks flying between us?",
    "💋 You’re the missing piece to my puzzle.",
    "🔥 Are you a light? Because you brighten up my world.",
    "🌼 If beauty were a crime, you’d be serving a life sentence.",
    "💖 Are you a puzzle? Because I’m falling for you piece by piece.",
    "🌹 Do you have a map? Because I keep getting lost in your eyes.",
    "💫 Is your name Wi-Fi? Because I’m feeling a connection.",
    "❤️ I’d say you’re one in a million, but you’re one in a lifetime.",
    "💘 If I could rearrange the alphabet, I’d put U and I together.",
    "🌟 Are you an angel? Because heaven is missing one.",
    "💋 Can I follow you home? Cause my parents always told me to follow my dreams.",
    "✨ You must be a diamond, because you’re one of a kind.",
    "💖 Are you a magnet? Because I’m drawn to you.",
    "🔥 You must be made of fire, because you're burning up my heart.",
    "🌼 You’re the reason my heart skips a beat.",
    "💋 You must be a dream, because I can’t believe you’re real.",
    "💘 Can I offer you a ride? Because my heart races for you.",
    "🌟 You light up my world like nobody else.",
    "💖 I just want to hold your hand and never let go."
]

tips_list = [
    "💬 Listen more, talk less — it’s sexy.",
    "🔥 Foreplay isn’t optional. It’s essential.",
    "💖 Compliment with intent, not habit.",
    "🎁 Surprise them — even with small things.",
    "💭 Explore fantasies together.",
    "👋 Little touches throughout the day build anticipation.",
    "💪 Confidence is the ultimate turn-on.",
    "👀 Be present, not distracted — attention is sexy.",
    "📝 Create memories, not just moments.",
    "😂 Laughter can be the best foreplay.",
    "✨ Compliment the way they make you feel, not just their looks.",
    "😏 Slow down, don't rush the good moments.",
    "💋 Always leave something to the imagination.",
    "💌 A handwritten note can be the most romantic gesture.",
    "💫 Share secrets to build a deeper connection.",
    "🎧 Music sets the mood. Curate a playlist together.",
    "🍷 Wine and conversation are a perfect pair.",
    "🕯️ Light candles to create a calming atmosphere.",
    "🎉 Make each day a mini celebration of each other.",
    "💑 Trust builds the best intimacy.",
    "📚 Learn together. Knowledge is sexy.",
    "🖤 The more you care, the more it shows in your touch.",
    "🎨 Try new things in the bedroom to keep the spark alive.",
    "🖋️ Write love letters. They never go out of style.",
    "🥂 Toast to each other — make each moment count.",
    "💬 Text sweet things in the middle of the day, just because.",
    "🌹 Leave little surprises around their space.",
    "🔒 Keep secrets, especially between the two of you.",
    "📅 Plan a surprise date night for no reason.",
    "📸 Capture spontaneous moments to remember the fun.",
    "🤝 Make them feel like a partner, not just a lover.",
    "🌌 Take time to stargaze together. It’s romantic.",
    "🎭 Try role-playing or dress-up for some added fun.",
    "👣 Walk barefoot together in nature — it’s grounding.",
    "🧸 Sometimes the simplest touch can say the most.",
    "🌟 Keep the romance alive, even after years together.",
    "🧡 When they’re feeling down, offer your support in subtle ways.",
    "🍫 Surprise them with their favorite treat, just because.",
    "💐 Give flowers for no reason other than to say you care.",
    "🏖️ Take a weekend getaway to rekindle the romance.",
    "💭 Remember the little things that make them happy.",
    "💘 Share your dreams with each other and build a future together.",
    "🛋️ Have a cozy night in — sometimes that’s all you need.",
    "🕵️‍♀️ Be curious about them, even after time together.",
    "🌞 Morning coffee or tea can be an intimate ritual.",
    "🎲 Play games that challenge you both, in and out of the bedroom.",
    "🔐 Protect the bond you share, and keep it private.",
    "🎶 Dance in the kitchen for no reason at all — it’s fun.",
    "🌹 Make each other feel special every single day.",
    "💃 Have a spontaneous dance party at home.",
    "📝 Leave a sweet note in their pocket for them to find later.",
    "🌸 Never underestimate the power of a thoughtful text."
]

truths = [
    "😏 What's your most secret desire?",
    "❤️ Have you ever had a crush on someone here?",
    "🙈 What’s the most embarrassing thing you've done?",
    "🌶️ What's the wildest fantasy you've ever had?",
    "🤥 Have you ever lied to get someone's attention?",
    "💋 What's your biggest turn-on?",
    "👀 If you had to kiss one person here, who would it be?",
    "🍕 What’s a guilty pleasure you haven't told anyone?",
    "💭 Who was your first crush?",
    "📱 Have you ever sent a risky text and regretted it?",
    "🫣 Have you ever had a crush on someone who didn’t know?",
    "💭 What’s your biggest turn-off?",
    "👀 What’s the worst date you’ve ever been on?",
    "🥺 What’s something you would do if no one was watching?",
    "🍸 If you could go on a date with anyone, who would it be?",
    "🌹 What’s the best compliment you’ve ever received?",
    "💎 What do you find most attractive in a person?",
    "💌 Have you ever sent someone a love letter?",
    "🔥 What’s the most romantic thing you’ve ever done?",
    "💃 Do you believe in love at first sight?",
    "🖤 Do you prefer deep conversations or light-hearted chats?",
    "🎲 What’s something you’ve always wanted to try but never did?",
    "📝 Do you keep a journal or diary?",
    "📚 What’s your most treasured book?",
    "🎤 Have you ever sung in front of an audience?",
    "💘 Have you ever been in love?",
    "😎 What’s the craziest thing you’ve done on a dare?",
    "💌 If you could date any fictional character, who would it be?",
    "🤔 What’s your idea of a perfect date?",
    "🌟 What’s the most spontaneous thing you’ve ever done?",
    "🎉 Have you ever done something embarrassing on purpose?",
    "🍒 What’s your ultimate guilty pleasure?",
    "🫣 Do you have any secret talents that no one knows about?",
    "🎁 What’s the best gift you’ve ever received?",
    "💭 If you could change one thing about yourself, what would it be?",
    "🤗 Do you believe in soulmates?",
    "⚡ What’s the most outrageous thing you’ve done for love?",
    "🎢 What’s the most adventurous thing you’ve ever done?",
    "🍯 Have you ever had a secret crush on a teacher or boss?",
    "🥀 What’s your idea of a perfect relationship?",
    "🦋 What’s your biggest pet peeve?",
    "🍷 Have you ever had a one-night stand?",
    "😚 What’s the cheesiest pickup line someone’s used on you?",
    "🚨 What’s the most illegal thing you’ve ever done?",
    "🧠 If you could switch lives with anyone for a day, who would it be?",
    "🎧 What’s your go-to karaoke song?",
    "🌙 Do you prefer morning or night time?",
    "🍓 What’s your favorite part of a romantic date?",
    "🚗 Have you ever kissed someone in a car?",
    "⛅ What’s something you wish you could tell someone, but you can’t?",
    "💭 What’s the last thing you do before bed?",
    "💪 Would you rather be super strong or super smart?"
]

dares = [
    "💌 Send a flirty emoji to the last person you chatted with.",
    "📱 Text 'I miss you' to someone unexpected.",
    "📸 Change your profile pic to something weird for 5 minutes.",
    "🎤 Record yourself saying something sexy and send it to a friend (voice note).",
    "💓 Send a heart emoji to the 3rd person in your chat list.",
    "📝 Describe your last dream in full detail to the group.",
    "🎭 Call someone and tell them you love them in a funny voice.",
    "🎤 Pretend you’re a celebrity giving an award speech for 30 seconds.",
    "🌐 Send a gif describing your mood right now.",
    "🎁 Give someone a random compliment.",
    "💋 Send a selfie with a silly face to someone.",
    "📸 Take a video of you doing a funny dance and send it to the group.",
    "💬 Send a message to someone you haven’t talked to in a while.",
    "🥳 Do your best dance moves on video and send it to the group.",
    "🤡 Send a picture of you making a silly face to someone.",
    "🕺 Call a friend and sing them a random song of your choice.",
    "👯 Take a picture of your shoes and send it to a friend.",
    "🥺 Send a voice message telling someone how much you appreciate them.",
    "💫 Post a silly story on your social media.",
    "💃 Record yourself doing 10 jumping jacks and send it to a friend.",
    "🌸 Share a childhood picture of yourself with the group.",
    "🍫 Send a message with a random fun fact you know.",
    "🎨 Draw something on paper and take a picture to share with the group.",
    "🎤 Sing a random karaoke song and send it to someone.",
    "📞 Send a message to your best friend saying, ‘I need a hug’!",
    "💌 Write a sweet note to someone and send it randomly.",
    "🔥 Send a funny meme to a friend.",
    "🍔 Record yourself eating something weird and send it to a friend.",
    "🎬 Re-enact a scene from your favorite movie and send it to someone.",
    "🎶 Record yourself singing a lullaby and send it to a friend.",
    "🌈 Take a photo of your socks and share it with the group.",
    "📷 Take a picture of the sunset and send it to a friend.",
    "🎤 Call someone and say a random sentence in a silly accent.",
    "🤳 Take a picture of your favorite spot in your room.",
    "🌟 Post an embarrassing video on your story.",
    "👀 Change your phone background to a funny image for the next 10 minutes.",
    "🧃 Send a voice note with the most random fact you can think of.",
    "🥳 Do a cartwheel and send a video of it to the group.",
    "📚 Share a motivational quote with a friend.",
    "🍕 Take a picture of the last meal you ate and share it.",
    "💄 Send a picture of your favorite lipstick shade.",
    "💃 Record a video of you doing a funny dance challenge.",
    "🍉 Share a silly meme with a friend.",
    "🐶 Pretend to be a dog for 30 seconds and send the video.",
    "🎧 Record your reaction to a song and share it with the group.",
    "🥱 Send a picture of you yawning to the group.",
    "🥓 Record yourself eating your favorite snack and send it to a friend.",
    "📚 Share a fun fact about yourself.",
    "🦸‍♂️ Pretend to be a superhero for 1 minute and send a video of it.",
    "💭 Share a childhood memory with the group.",
    "🎲 Tell a joke and send it to a friend.",
    "🍀 Send a screenshot of your most embarrassing text to a friend.",
    "💬 Text your crush a random compliment.",
    "📷 Take a picture of something funny in your room and send it to the group.",
    "💡 Share a lightbulb moment you had recently."
]

slaps = [
    "👋 *slaps you with love*—don't make me do it again!",
    "💥 *slaps you dramatically* as if the world depends on it!",
    "🔥 *slaps you with a passion* you didn't know existed!",
    "🍑 *slaps you on your behind*—that was for the fun of it!",
    "🥴 *slaps you with confusion*—what were you thinking?!",
    "💪 *slaps you with strength*—that's how it's done!",
    "⚡ *slaps you like a jolt of electricity*—zap!",
    "🌪️ *slaps you with the force of a tornado*—watch out!",
    "🥂 *slaps you with a toast*—cheers to your awesomeness!",
    "⚡ *slaps you with a shocking twist*—you didn’t see that coming!",
    "💥 *slaps you like a thunderstorm*—POW!",
    "💀 *slaps you with dark energy*—why so serious?",
    "💋 *slaps you with a kiss*—it’s a sweet one, trust me.",
    "🎭 *slaps you like it’s a Shakespearean play*—where art thou, Romeo?",
    "👀 *slaps you to wake up from your dreams*—hello?!",
    "💥 *slaps you with the intensity of a hurricane*—hold on!",
    "🖤 *slaps you with sarcasm*—because you needed that!",
    "🌠 *slaps you like a falling star*—catch that!",
    "🐉 *slaps you with the power of a dragon*—ROAR!",
    "👑 *slaps you like royalty*—how dare you!",
    "🌌 *slaps you with cosmic energy*—we're all just stardust.",
    "🎮 *slaps you like a video game boss*—you're not winning this time.",
    "🎩 *slaps you like a magician*—now you see it, now you don’t!",
    "🎤 *slaps you with a mic drop*—boom, mind blown!",
    "💎 *slaps you like a precious jewel*—worth every second.",
    "🥂 *slaps you with elegance*—classy, just classy.",
    "🍩 *slaps you with sweetness*—because you’re too sweet to resist.",
    "💀 *slaps you like a ghost*—you didn’t even feel it coming!",
    "🎩 *slaps you like a grand illusion*—whoops, sorry!",
    "🎶 *slaps you like a dance move*—now follow my lead!",
    "🌑 *slaps you with mystery*—dark and ominous.",
    "🔥 *slaps you with fiery passion*—the heat is on!",
    "🎉 *slaps you with celebration*—time to party!",
    "💣 *slaps you with a blast of power*—BOOM!",
    "🎁 *slaps you with a gift*—you didn’t expect that, huh?",
    "🦄 *slaps you with a magical touch*—prestidigitation at its finest.",
    "🌟 *slaps you like a shooting star*—make a wish!",
    "🎠 *slaps you like you’re on a rollercoaster*—hold tight!",
    "🍿 *slaps you like a movie moment*—cut to black!",
    "⚔️ *slaps you like a knight in shining armor*—prepare yourself!",
    "💥 *slaps you like a superhero landing*—expect the dramatic flair.",
    "🍁 *slaps you with nature’s touch*—wind through the trees!",
    "🥳 *slaps you with excitement*—let’s go wild!",
    "⚓ *slaps you like a sailor’s goodbye*—take care, mate!",
    "🍷 *slaps you with sophistication*—savor the taste.",
    "💎 *slaps you with precious confidence*—you got this!",
    "🛸 *slaps you with extraterrestrial vibes*—get ready for takeoff!",
    "🦇 *slaps you like a spooky ghost*—BOO!",
    "💪 *slaps you with pure strength*—don’t test me!",
    "👽 *slaps you like an alien encounter*—you’re not from around here, are you?",
    "🎬 *slaps you with an epic scene*—take a bow, it’s your moment!",
    "🎤 *slaps you like a karaoke superstar*—it’s your stage now!",
    "🌈 *slaps you with colorful joy*—bring on the rainbow!",
    "💫 *slaps you with sparkling stardust*—shine bright!",
    "🔮 *slaps you with mystery*—prepare for the unknown!",
    "🦋 *slaps you with lightness*—like a butterfly kiss!",
    "🌪️ *slaps you with a tornado of feelings*—hold on to your emotions!"
]

# RANDOM FUNCTIONS
async def facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_then_reply(update, context, random.choice(facts_list))

async def flirt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_then_reply(update, context, random.choice(flirt_list))

async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_typing_then_reply(update, context, random.choice(tips_list))

# ROAST
async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        name = user.mention_html()
        reply_to = update.message.reply_to_message.message_id
    elif context.args:
        name = " ".join(context.args)
        reply_to = None
    else:
        await send_typing_then_reply(update, context, "Please provide a name or reply to someone!")
        return

    await send_typing_then_reply(update, context, f"{name}, {random.choice(roast_list)}", reply_to_message_id=reply_to)

# TRUTH, DARE, SLAP
async def t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(truths)
    reply_to = update.message.reply_to_message.message_id if update.message.reply_to_message else None
    await send_typing_then_reply(update, context, msg, reply_to_message_id=reply_to)

async def d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(dares)
    reply_to = update.message.reply_to_message.message_id if update.message.reply_to_message else None
    await send_typing_then_reply(update, context, msg, reply_to_message_id=reply_to)

async def slap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        name = user.mention_html()
        msg = f"{name}, {random.choice(slaps)}"
        reply_to = update.message.reply_to_message.message_id
    else:
        msg = random.choice(slaps)
        reply_to = None

    await send_typing_then_reply(update, context, msg, reply_to_message_id=reply_to)

# APP SETUP
app = ApplicationBuilder().token(TOKEN).build()

# COMMAND HANDLERS
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("love", love))
app.add_handler(CommandHandler("horny", horny))
app.add_handler(CommandHandler("pervy", pervy))
app.add_handler(CommandHandler("sexrate", sexrate))
app.add_handler(CommandHandler("facts", facts))
app.add_handler(CommandHandler("roast", roast))
app.add_handler(CommandHandler("flirt", flirt))
app.add_handler(CommandHandler("tips", tips))
app.add_handler(CommandHandler("t", t))
app.add_handler(CommandHandler("d", d))
app.add_handler(CommandHandler("slap", slap))

# RUN
app.run_polling()

if __name__ == "__main__":
    main()