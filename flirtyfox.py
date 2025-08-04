import os
import time
import random
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Bot configuration settings
TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
PORT = int(os.environ.get("PORT", 10000))
UPDATES_URL = os.environ.get("UPDATES_URL", "https://t.me/WorkGlows")
SUPPORT_URL = os.environ.get("SUPPORT_URL", "https://t.me/SoulMeetsHQ")

# Basic logging setup
logging.basicConfig(level=logging.INFO)

# Bot text messages
BOT_MESSAGES = {
    "welcome": """Hey there, {user}! 🦊💕

I'm Flirty Fox, your cheeky companion for all things fun and flirty! 

Ready to spice up your day with some playful banter? Let's get this party started! 🎉✨""",
    "provide_name": "Please provide a name or reply to someone!",
    "pinging": "🛰️ Pinging...",
    "pong": "🏓 <a href=\"https://t.me/SoulMeetsHQ\">Pong!</a> {latency}ms"
}

# Random image URLs
IMAGES = [
    "https://ik.imagekit.io/asadofc/Images1.png",
    "https://ik.imagekit.io/asadofc/Images2.png",
    "https://ik.imagekit.io/asadofc/Images3.png",
    "https://ik.imagekit.io/asadofc/Images4.png",
    "https://ik.imagekit.io/asadofc/Images5.png",
    "https://ik.imagekit.io/asadofc/Images6.png",
    "https://ik.imagekit.io/asadofc/Images7.png",
    "https://ik.imagekit.io/asadofc/Images8.png",
    "https://ik.imagekit.io/asadofc/Images9.png",
    "https://ik.imagekit.io/asadofc/Images10.png",
    "https://ik.imagekit.io/asadofc/Images11.png",
    "https://ik.imagekit.io/asadofc/Images12.png",
    "https://ik.imagekit.io/asadofc/Images13.png",
    "https://ik.imagekit.io/asadofc/Images14.png",
    "https://ik.imagekit.io/asadofc/Images15.png",
    "https://ik.imagekit.io/asadofc/Images16.png",
    "https://ik.imagekit.io/asadofc/Images17.png",
    "https://ik.imagekit.io/asadofc/Images18.png",
    "https://ik.imagekit.io/asadofc/Images19.png",
    "https://ik.imagekit.io/asadofc/Images20.png",
    "https://ik.imagekit.io/asadofc/Images21.png",
    "https://ik.imagekit.io/asadofc/Images22.png",
    "https://ik.imagekit.io/asadofc/Images23.png",
    "https://ik.imagekit.io/asadofc/Images24.png",
    "https://ik.imagekit.io/asadofc/Images25.png",
    "https://ik.imagekit.io/asadofc/Images26.png",
    "https://ik.imagekit.io/asadofc/Images27.png",
    "https://ik.imagekit.io/asadofc/Images28.png",
    "https://ik.imagekit.io/asadofc/Images29.png",
    "https://ik.imagekit.io/asadofc/Images30.png",
    "https://ik.imagekit.io/asadofc/Images31.png",
    "https://ik.imagekit.io/asadofc/Images32.png",
    "https://ik.imagekit.io/asadofc/Images33.png",
    "https://ik.imagekit.io/asadofc/Images34.png",
    "https://ik.imagekit.io/asadofc/Images35.png",
    "https://ik.imagekit.io/asadofc/Images36.png",
    "https://ik.imagekit.io/asadofc/Images37.png",
    "https://ik.imagekit.io/asadofc/Images38.png",
    "https://ik.imagekit.io/asadofc/Images39.png",
    "https://ik.imagekit.io/asadofc/Images40.png"
]

# Romantic fun facts
FACTS_LIST = [
    "❤️ Kissing can burn up to 6 calories a minute!",
    "💋 Your lips are 100 times more sensitive than your fingertips.",
    "🧠 Falling in love has neurological effects similar to cocaine.",
    "💕 Couples who hold hands have synchronized heartbeats.",
    "🌹 The smell of roses can boost your libido.",
    "😍 Looking into someone's eyes for 4 minutes can make you fall in love.",
    "💘 Chocolate releases the same chemicals as falling in love."
]

# Witty roast messages
ROAST_LIST = [
    "😂 You're like a cloud. When you disappear, it's a beautiful day.",
    "🔥 I'd roast you, but my mom said I shouldn't burn trash.",
    "😏 You're the reason gene pools need lifeguards.",
    "💀 If laughter is the best medicine, your face must be curing the world.",
    "🎭 You're not stupid; you just have bad luck thinking.",
    "🌟 You're like a shooting star - everyone wishes you'd disappear.",
    "💡 You're so bright, you make the sun jealous... of your stupidity."
]

# Flirty pickup lines
FLIRT_LIST = [
    "😍 Are you a magician? Because whenever I look at you, everyone else disappears.",
    "🔥 Do you have a map? I keep getting lost in your eyes.",
    "💕 Are you Wi-Fi? Because I'm feeling a connection.",
    "🌟 If you were a vegetable, you'd be a cute-cumber.",
    "💋 Are you made of copper and tellurium? Because you're Cu-Te.",
    "😘 Do you believe in love at first sight, or should I walk by again?",
    "💘 Are you a parking ticket? Because you've got 'fine' written all over you."
]

# Romance dating tips
TIPS_LIST = [
    "💬 Listen more, talk less - it's sexy.",
    "🔥 Foreplay isn't optional. It's essential.",
    "👁️ Eye contact during conversations increases attraction by 30%.",
    "💋 Light touches on the arm can increase romantic interest.",
    "🌹 Surprise dates are more memorable than expensive ones.",
    "😊 Genuine compliments are more effective than generic ones.",
    "💕 Shared experiences create stronger bonds than material gifts."
]

# Truth game questions
TRUTHS = [
    "😏 What's your most secret desire?",
    "💋 What's the most romantic thing someone has done for you?",
    "🔥 What's your biggest turn-on?",
    "💕 Have you ever had a crush on someone in this group?",
    "😍 What's the sexiest quality someone can have?",
    "💘 What's your ideal first date?",
    "🌟 What's something you've never told anyone?"
]

# Dare game challenges
DARES = [
    "💌 Send a flirty emoji to the last person you chatted with.",
    "😘 Give someone in the group a virtual kiss.",
    "🔥 Post a story saying 'I'm single and ready to mingle' for 5 minutes.",
    "💋 Send a voice note saying 'Hey gorgeous' to your crush.",
    "😍 Change your profile picture to a selfie with a wink.",
    "💕 Text your ex 'I miss you' then immediately say 'Sorry, wrong person'.",
    "🌹 Compliment the person above you in the most flirty way possible."
]

# Playful slap responses
SLAPS = [
    "👋 Slaps you with love - don't make me do it again!",
    "🤚 *SLAP* That's for being too cute!",
    "✋ Gets slapped back to reality!",
    "👋 *Slaps gently* Wake up, sunshine!",
    "🤚 Slaps you with a bouquet of roses!",
    "✋ *SLAP* That's what you get for being awesome!",
    "👋 Gets a love slap - the best kind!"
]

# Percentage feedback messages
FEEDBACK_MESSAGES = {
    "low": "Not impressive... Needs some work!",
    "below_average": "Hmm, you're getting there!",
    "average": "Decent! You've got potential.",
    "good": "Ooh, quite spicy! Keep it up!",
    "excellent": "You're an absolute legend at this!"
}

# Available bot commands
COMMANDS = {
    "start": "🏠 Bot welcome message",
    "love": "💖 Love percentage check",
    "horny": "🥵 Horny level meter",
    "pervy": "🤤 Pervy level check", 
    "sex": "🔥 Sexual prowess rating",
    "facts": "💌 Romantic fun facts",
    "roast": "💥 Witty roast generator",
    "flirt": "💘 Flirty pickup lines",
    "tips": "💡 Romance dating tips",
    "t": "❓ Truth question game",
    "d": "🎲 Dare challenge game", 
    "slap": "👋 Playful slap reply"
}

# Get percentage feedback
def get_feedback(percent):
    if percent <= 20:
        return FEEDBACK_MESSAGES["low"]
    elif percent <= 40:
        return FEEDBACK_MESSAGES["below_average"]
    elif percent <= 60:
        return FEEDBACK_MESSAGES["average"]
    elif percent <= 80:
        return FEEDBACK_MESSAGES["good"]
    else:
        return FEEDBACK_MESSAGES["excellent"]

# Extract user info
def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        name = user.mention_html()
        reply_to = update.message.reply_to_message.message_id
    elif context.args:
        name = " ".join(context.args)
        reply_to = None
    else:
        return None, None
    
    return name, reply_to

# Welcome command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    welcome_msg = BOT_MESSAGES["welcome"].format(user=user.mention_html())
    
    # Get dynamic username
    bot_info = await context.bot.get_me()
    bot_username = bot_info.username

    keyboard = [
        [
            InlineKeyboardButton("Updates", url=UPDATES_URL),
            InlineKeyboardButton("Support", url=SUPPORT_URL),
        ],
        [
            InlineKeyboardButton("Add Me To Your Group", url=f"https://t.me/{bot_username}?startgroup=true"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send random image
    random_image = random.choice(IMAGES)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=random_image,
        caption=welcome_msg,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

# Ping latency command
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    
    # Check chat type
    is_private = update.effective_chat.type == 'private'
    
    if is_private:
        # Private chat message
        message = await update.message.reply_html(BOT_MESSAGES["pinging"])
    else:
        # Group reply message
        message = await update.message.reply_html(
            BOT_MESSAGES["pinging"], 
            reply_to_message_id=update.message.message_id
        )
    
    # Calculate response latency
    end_time = time.time()
    latency = round((end_time - start_time) * 1000, 2)
    
    # Edit with pong
    pong_message = BOT_MESSAGES["pong"].format(latency=latency)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message.message_id,
        text=pong_message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

# Handle percentage commands
async def handle_random_percent(update: Update, context: ContextTypes.DEFAULT_TYPE, label: str):
    name, reply_to = get_user_info(update, context)
    
    if not name:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        await update.message.reply_html(BOT_MESSAGES["provide_name"])
        return

    percent = random.randint(10, 100)
    feedback = get_feedback(percent)
    message = f"{name}, your {label} level is {percent}%\n\n{feedback}"
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_html(
        text=message,
        reply_to_message_id=reply_to
    )

# Love percentage command
async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "love")

# Horny level command
async def horny(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "horny")

# Pervy level command
async def pervy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "pervy")

# Sex rating command
async def sex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "sex")

# Random facts command
async def facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_html(random.choice(FACTS_LIST))

# Flirt lines command
async def flirt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_html(random.choice(FLIRT_LIST))

# Romance tips command
async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_html(random.choice(TIPS_LIST))

# Roast someone command
async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name, reply_to = get_user_info(update, context)
    
    if not name:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        await update.message.reply_html(BOT_MESSAGES["provide_name"])
        return

    message = f"{name}, {random.choice(ROAST_LIST)}"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_html(
        text=message,
        reply_to_message_id=reply_to
    )

# Truth question command
async def t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(TRUTHS)
    reply_to = update.message.reply_to_message.message_id if update.message.reply_to_message else None
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_html(
        text=msg,
        reply_to_message_id=reply_to
    )

# Dare challenge command
async def d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(DARES)
    reply_to = update.message.reply_to_message.message_id if update.message.reply_to_message else None
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_html(
        text=msg,
        reply_to_message_id=reply_to
    )

# Slap someone command
async def slap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        name = user.mention_html()
        msg = f"{name}, {random.choice(SLAPS)}"
        reply_to = update.message.reply_to_message.message_id
    else:
        msg = random.choice(SLAPS)
        reply_to = None

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await update.message.reply_html(
        text=msg,
        reply_to_message_id=reply_to
    )

# HTTP server handler
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Flirty Fox Bot is alive!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        pass

# Start HTTP server
def start_dummy_server():
    server = HTTPServer(("0.0.0.0", PORT), DummyHandler)
    print(f"Dummy server listening on port {PORT}")
    server.serve_forever()

# Main bot function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("love", love))
    app.add_handler(CommandHandler("horny", horny))
    app.add_handler(CommandHandler("pervy", pervy))
    app.add_handler(CommandHandler("sex", sex))
    app.add_handler(CommandHandler("facts", facts))
    app.add_handler(CommandHandler("roast", roast))
    app.add_handler(CommandHandler("flirt", flirt))
    app.add_handler(CommandHandler("tips", tips))
    app.add_handler(CommandHandler("t", t))
    app.add_handler(CommandHandler("d", d))
    app.add_handler(CommandHandler("slap", slap))

    print("Flirty Fox Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    # Start HTTP server
    threading.Thread(target=start_dummy_server, daemon=True).start()
    
    # Start the bot
    main()