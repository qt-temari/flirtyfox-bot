import os
import time
import random
import logging
import threading
import aiohttp
import asyncio
import traceback
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import TelegramError, NetworkError, BadRequest, Forbidden
from typing import Dict, Optional, Tuple, Any
from datetime import datetime

# Environment variables configuration
TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
PORT = int(os.environ.get("PORT", 10000))
UPDATES_URL = os.environ.get("UPDATES_URL", "https://t.me/WorkGlows")
SUPPORT_URL = os.environ.get("SUPPORT_URL", "https://t.me/SoulMeetsHQ")
NINJA_API_KEY = os.environ.get("NINJA_API_KEY", "W/cYCzw1s5xXZqRbQafNXA==BxUt1niLMg2M9FgS")
API_TIMEOUT = int(os.environ.get("API_TIMEOUT", "8"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Updated API endpoints with working alternatives
API_ENDPOINTS = {
    "ninja_facts": "https://api.api-ninjas.com/v1/facts",
    "ninja_jokes": "https://api.api-ninjas.com/v1/jokes",
    "ninja_quotes": "https://api.api-ninjas.com/v1/quotes",
    "dad_jokes": "https://icanhazdadjoke.com/",
    "chuck_norris": "https://api.chucknorris.io/jokes/random",
    "advice": "https://api.adviceslip.com/advice",
    "quotable": "https://api.quotable.io/random",
    "cat_facts": "https://catfact.ninja/fact",
    "dog_facts": "https://dogapi.dog/api/v2/facts",
    "useless_facts": "https://uselessfacts.jsph.pl/random.json?language=en",
    "affirmations": "https://www.affirmations.dev/",
    "kanye_quotes": "https://api.kanye.rest/",
    "programming_quotes": "https://programming-quotes-api.herokuapp.com/Quotes/random"
}

# Bot messages dictionary
BOT_MESSAGES = {
    "welcome": """Hey there, {user}! 🦊💕

I'm Flirty Fox, your cheeky companion for all things fun and flirty! 

Ready to spice up your day with some playful banter? Let's get this party started! 🎉✨""",
    "provide_name": "Please provide a name or reply to someone!",
    "pinging": "🛰️ Pinging...",
    "pong": "🏓 <a href=\"https://t.me/SoulMeetsHQ\">Pong!</a> {latency}ms",
    "error_occurred": "😅 Oops! Something went wrong. Please try again later!",
    "api_error": "🌐 Having trouble connecting to external services. Using fallback content!",
    "rate_limit": "⏰ Slow down there, tiger! Please wait a moment before trying again.",
}

# Available bot commands
COMMANDS = {
    "start": "🏠 Bot welcome message",
    "love": "💖 Love percentage check",
    "horny": "🥵 Horny level meter",
    "pervy": "🤤 Pervy level check", 
    "sex": "🔥 Sexual prowess rating",
    "facts": "💌 Random interesting facts",
    "roast": "💥 Witty roast generator",
    "flirt": "💘 Flirty pickup lines",
    "tips": "💡 Romance dating advice",
    "quote": "✨ Inspirational quotes",
    "joke": "😂 Random jokes",
    "compliment": "😊 Sweet compliments",
    "t": "❓ Truth question game",
    "d": "🎲 Dare challenge game", 
    "slap": "👋 Playful slap reply",
    "ping": "🏓 Check bot latency"
}

# Percentage feedback messages
FEEDBACK_MESSAGES = {
    "low": "Not impressive... Needs some work!",
    "below_average": "Hmm, you're getting there!",
    "average": "Decent! You've got potential.",
    "good": "Ooh, quite spicy! Keep it up!",
    "excellent": "You're an absolute legend at this!"
}

# Random image URLs list
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
    "https://ik.imagekit.io/asadofc/Images10.png"
]

# Enhanced romantic facts list
FACTS_LIST = [
    "❤️ Kissing can burn up to 6 calories a minute!",
    "💋 Your lips are 100 times more sensitive than your fingertips.",
    "🧠 Falling in love has neurological effects similar to cocaine.",
    "💕 Couples who hold hands have synchronized heartbeats.",
    "🌹 The smell of roses can boost your libido.",
    "😍 Looking into someone's eyes for 4 minutes can make you fall in love.",
    "💘 Chocolate releases the same chemicals as falling in love.",
    "🔥 The heart symbol (♥) actually represents the shape of ivy leaves.",
    "💖 Hugging for 20 seconds releases oxytocin, the 'love hormone'.",
    "🎵 Listening to music together synchronizes heartbeats.",
    "💌 Love letters activate the same brain regions as cocaine.",
    "🦋 'Butterflies in stomach' are real stress hormones from attraction."
]

# Enhanced witty roast messages list
ROAST_LIST = [
    "😂 You're like a cloud. When you disappear, it's a beautiful day.",
    "🔥 I'd roast you, but my mom said I shouldn't burn trash.",
    "😏 You're the reason gene pools need lifeguards.",
    "💀 If laughter is the best medicine, your face must be curing the world.",
    "🎭 You're not stupid; you just have bad luck thinking.",
    "🌟 You're like a shooting star - everyone wishes you'd disappear.",
    "💡 You're so bright, you make the sun jealous... of your stupidity.",
    "🎪 You're like a circus - entertaining, but I wouldn't want to live there.",
    "🏆 Congratulations! You've achieved peak mediocrity.",
    "🔍 I'd explain it to you, but I don't have any crayons with me."
]

# Enhanced flirty pickup lines list
FLIRT_LIST = [
    "😍 Are you a magician? Because whenever I look at you, everyone else disappears.",
    "🔥 Do you have a map? I keep getting lost in your eyes.",
    "💕 Are you Wi-Fi? Because I'm feeling a connection.",
    "🌟 If you were a vegetable, you'd be a cute-cumber.",
    "💋 Are you made of copper and tellurium? Because you're Cu-Te.",
    "😘 Do you believe in love at first sight, or should I walk by again?",
    "💘 Are you a parking ticket? Because you've got 'fine' written all over you.",
    "⚡ Are you a thunderstorm? Because you're electrifying.",
    "🍯 Are you honey? Because you're sweet and I'm stuck on you.",
    "🌙 Are you the moon? Because even in darkness, you light up my world."
]

# Enhanced romance dating tips list
TIPS_LIST = [
    "💬 Listen more, talk less - it's incredibly attractive.",
    "🔥 Genuine interest beats expensive gifts every time.",
    "👁️ Eye contact during conversations increases attraction by 30%.",
    "💋 Light, respectful touches on the arm can increase romantic interest.",
    "🌹 Surprise dates create more memorable experiences than expensive ones.",
    "😊 Specific compliments are 10x more effective than generic ones.",
    "💕 Shared experiences create stronger bonds than material gifts.",
    "📱 Put your phone away during dates - presence is the best present.",
    "🎭 Be genuinely yourself - authenticity is magnetic.",
    "⏰ Quality time together trumps quantity every time."
]

# Enhanced truth game questions list
TRUTHS = [
    "😏 What's your most secret desire that you've never told anyone?",
    "💋 What's the most romantic thing someone has ever done for you?",
    "🔥 What's your biggest turn-on in a potential partner?",
    "💕 Have you ever had a crush on someone in this group?",
    "😍 What's the sexiest quality someone can have?",
    "💘 Describe your ideal romantic date in detail.",
    "🌟 What's something about love that you've never shared?",
    "💌 What's the most embarrassing thing you've done for love?",
    "🎯 What's your love language and why?",
    "💖 What's your biggest relationship dealbreaker?"
]

# Enhanced dare challenge list
DARES = [
    "💌 Send a flirty emoji to the last person you chatted with.",
    "😘 Give someone in the group a virtual kiss with a voice note.",
    "🔥 Post a story saying 'Single and ready to mingle' for 10 minutes.",
    "💋 Send a voice note saying 'Hey gorgeous' to your crush.",
    "😍 Change your profile picture to your most attractive selfie.",
    "💕 Text your ex 'Thinking of you' then say 'Wrong person' after 5 minutes.",
    "🌹 Give the most flirty compliment to the person above you.",
    "💃 Record a 10-second dance and send it to your crush.",
    "🎭 Change your status to 'Looking for my soulmate' for an hour.",
    "💘 Write a romantic poem and share it with the group."
]

# Enhanced playful slap responses list
SLAPS = [
    "👋 *Slaps you with love* - Don't make me do it again!",
    "🤚 *GENTLE SLAP* That's for being too cute to handle!",
    "✋ *Gets slapped back to reality* - Wake up, dreamer!",
    "👋 *Slaps gently* Rise and shine, sunshine!",
    "🤚 *Slaps you with a bouquet of virtual roses*",
    "✋ *LOVE SLAP* That's what you get for being awesome!",
    "👋 *Gets a playful reality check* - The best kind!",
    "🤚 *Slaps away your bad vibes* - Only good energy here!",
    "✋ *WAKE UP SLAP* Time to face how amazing you are!",
    "👋 *Slaps you with motivation* - Go conquer the world!"
]

# Enhanced fallback quotes list
FALLBACK_QUOTES = [
    "✨ \"Love is not about possession, it's about appreciation.\" - Unknown",
    "💕 \"The best relationships are built on friendship first.\" - Wisdom",
    "🌟 \"Be yourself; everyone else is already taken.\" - Oscar Wilde",
    "💖 \"Love yourself first, and everything else falls into place.\" - Truth",
    "🔥 \"Passion is energy. Feel the power that comes from focusing on what excites you.\" - Oprah",
    "💘 \"Love is composed of a single soul inhabiting two bodies.\" - Aristotle",
    "🌹 \"Where there is love, there is life.\" - Gandhi",
    "💌 \"The greatest thing you'll ever learn is to love and be loved in return.\" - Eden Ahbez"
]

# Enhanced fallback compliments list
FALLBACK_COMPLIMENTS = [
    "😍 You're absolutely stunning and your energy is infectious!",
    "✨ Your smile could literally light up the entire universe!",
    "💖 You have such a beautiful soul that radiates warmth!",
    "🌟 You're incredibly amazing just the way you are - never change!",
    "💕 Your positive energy is absolutely contagious and uplifting!",
    "🔥 You have this magnetic charm that draws everyone to you!",
    "🌹 Your kindness and beauty make the world a better place!",
    "💫 You're one of those rare people who make others feel special!",
    "🦋 Your personality is as beautiful as your appearance!",
    "💎 You're a rare gem in a world full of ordinary stones!"
]

# Color codes for enhanced logging
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Colors.GREEN,
        'INFO': Colors.CYAN,
        'WARNING': Colors.YELLOW,
        'ERROR': Colors.RED,
        'CRITICAL': Colors.PURPLE,
    }

    def format(self, record):
        original_format = super().format(record)
        color = self.COLORS.get(record.levelname, Colors.RESET)
        colored_format = f"{color}{original_format}{Colors.RESET}"
        return colored_format

def setup_colored_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = ColoredFormatter(
        fmt='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

logger = setup_colored_logging()

def extract_user_info(msg: Message) -> Dict[str, any]:
    try:
        logger.debug("🔍 Extracting user information from message")
        u = msg.from_user
        c = msg.chat
        
        if not u or not c:
            logger.error("❌ Message missing user or chat")
            return {}
            
        info = {
            "user_id": u.id,
            "username": u.username or "No Username",
            "full_name": u.full_name or "No Name",
            "chat_id": c.id,
            "chat_type": c.type.value if hasattr(c.type, 'value') else str(c.type),
            "chat_title": c.title or c.first_name or "No Title",
            "chat_username": f"@{c.username}" if c.username else "No Username",
            "chat_link": f"https://t.me/{c.username}" if c.username else "No Link",
        }
        logger.info(
            f"📑 User info extracted: {info['full_name']} (@{info['username']}) "
            f"[ID: {info['user_id']}] in {info['chat_title']} [{info['chat_id']}]"
        )
        return info
    except Exception as e:
        logger.error(f"❌ Error extracting user info: {str(e)}")
        return {}

def log_with_user_info(level: str, message: str, user_info: Dict[str, any]) -> None:
    try:
        if not user_info:
            user_detail = "👤 Unknown User | 💬 Unknown Chat"
        else:
            user_detail = (
                f"👤 {user_info.get('full_name', 'Unknown')} (@{user_info.get('username', 'Unknown')}) | "
                f"💬 {user_info.get('chat_title', 'Unknown')} [{user_info.get('chat_type', 'Unknown')}]"
            )
            
        full_message = f"{message} | {user_detail}"

        level_upper = level.upper()
        if level_upper == "INFO":
            logger.info(full_message)
        elif level_upper == "DEBUG":
            logger.debug(full_message)
        elif level_upper == "WARNING":
            logger.warning(full_message)
        elif level_upper == "ERROR":
            logger.error(full_message)
        else:
            logger.info(full_message)
            
    except Exception as e:
        logger.error(f"❌ Error in log_with_user_info: {str(e)}")

def get_feedback(percent: int) -> str:
    try:
        if not isinstance(percent, int):
            percent = int(percent)
            
        percent = max(0, min(100, percent))
        
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
            
    except Exception as e:
        logger.error(f"❌ Error getting feedback: {str(e)}")
        return "Something's not quite right, but you're awesome anyway!"

def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Tuple[Optional[str], Optional[int]]:
    try:
        if not update or not update.message:
            return None, None
            
        user_info = extract_user_info(update.message)
        
        if update.message.reply_to_message:
            reply_msg = update.message.reply_to_message
            if not reply_msg.from_user:
                return None, None
                
            user = reply_msg.from_user
            name = user.mention_html() if user.mention_html else f"@{user.username}" if user.username else user.full_name
            reply_to = reply_msg.message_id
            return name, reply_to
            
        elif context and context.args:
            if not isinstance(context.args, list):
                return None, None
                
            name = " ".join(context.args).strip()
            if not name:
                return None, None
                
            return name, None
        else:
            return None, None
            
    except Exception as e:
        logger.error(f"❌ Error in get_user_info: {str(e)}")
        return None, None

async def fetch_api_data(url: str, headers: dict = None, timeout: int = API_TIMEOUT) -> Optional[dict]:
    try:
        logger.debug(f"🌐 Fetching from: {url}")
        
        if not url:
            return None
            
        if headers is None:
            headers = {}
        headers.update({
            'User-Agent': 'FlirtyFoxBot/2.0 (Telegram Bot)',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        
        connector = aiohttp.TCPConnector(
            limit=10, 
            ttl_dns_cache=300, 
            use_dns_cache=True,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        timeout_config = aiohttp.ClientTimeout(total=timeout, connect=5)
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout_config,
            headers=headers
        ) as session:
            async with session.get(url) as response:
                logger.debug(f"📊 Response status: {response.status}")
                
                if response.status == 200:
                    content_type = response.headers.get('content-type', '').lower()
                    if 'application/json' in content_type:
                        data = await response.json()
                        logger.info(f"✅ API fetch successful from: {url}")
                        return data
                    else:
                        logger.warning(f"⚠️ Non-JSON response from: {url}")
                        return None
                elif response.status == 429:
                    logger.warning(f"⚠️ Rate limited by API: {url}")
                    return None
                elif response.status == 404:
                    logger.warning(f"⚠️ API endpoint not found: {url}")
                    return None
                else:
                    logger.warning(f"⚠️ HTTP {response.status} from: {url}")
                    return None
                    
    except asyncio.TimeoutError:
        logger.error(f"⏰ Timeout fetching from: {url}")
        return None
    except aiohttp.ClientError as e:
        logger.error(f"🌐 Client error fetching from {url}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"❌ Unexpected error fetching from {url}: {str(e)}")
        return None

async def get_ninja_api_data(endpoint: str, category: str = None) -> Optional[dict]:
    try:
        if not endpoint or not NINJA_API_KEY:
            return None
        
        headers = {
            'X-Api-Key': NINJA_API_KEY,
            'Content-Type': 'application/json'
        }
        
        url = endpoint
        if category:
            url += f"?category={category}"
        
        return await fetch_api_data(url, headers)
        
    except Exception as e:
        logger.error(f"❌ Error in get_ninja_api_data: {str(e)}")
        return None

async def get_random_fact() -> str:
    try:
        logger.debug("🧠 Getting random fact")
        
        # Try multiple fact APIs
        fact_apis = [
            ("ninja", API_ENDPOINTS["ninja_facts"]),
            ("useless", API_ENDPOINTS["useless_facts"]),
            ("cat", API_ENDPOINTS["cat_facts"])
        ]
        
        for api_name, url in fact_apis:
            try:
                if api_name == "ninja":
                    data = await get_ninja_api_data(url)
                    if data and isinstance(data, list) and len(data) > 0 and 'fact' in data[0]:
                        return f"🧠 {data[0]['fact']}"
                elif api_name == "useless":
                    data = await fetch_api_data(url)
                    if data and isinstance(data, dict) and 'text' in data:
                        return f"🤓 {data['text']}"
                elif api_name == "cat":
                    data = await fetch_api_data(url)
                    if data and isinstance(data, dict) and 'fact' in data:
                        return f"🐱 {data['fact']}"
            except Exception as e:
                logger.debug(f"⚠️ {api_name} API failed: {str(e)}")
                continue
        
        return random.choice(FACTS_LIST)
        
    except Exception as e:
        logger.error(f"❌ Error in get_random_fact: {str(e)}")
        return random.choice(FACTS_LIST)

async def get_random_joke() -> str:
    try:
        logger.debug("😂 Getting random joke")
        
        # Try multiple joke APIs
        joke_apis = [
            ("ninja", API_ENDPOINTS["ninja_jokes"]),
            ("dad", API_ENDPOINTS["dad_jokes"]),
            ("chuck", API_ENDPOINTS["chuck_norris"])
        ]
        
        for api_name, url in joke_apis:
            try:
                if api_name == "ninja":
                    data = await get_ninja_api_data(url)
                    if data and isinstance(data, list) and len(data) > 0 and 'joke' in data[0]:
                        return f"😂 {data[0]['joke']}"
                elif api_name == "dad":
                    headers = {'Accept': 'application/json'}
                    data = await fetch_api_data(url, headers)
                    if data and isinstance(data, dict) and 'joke' in data:
                        return f"👨‍💼 {data['joke']}"
                elif api_name == "chuck":
                    data = await fetch_api_data(url)
                    if data and isinstance(data, dict) and 'value' in data:
                        return f"💪 {data['value']}"
            except Exception as e:
                logger.debug(f"⚠️ {api_name} API failed: {str(e)}")
                continue
        
        return random.choice(ROAST_LIST)
        
    except Exception as e:
        logger.error(f"❌ Error in get_random_joke: {str(e)}")
        return random.choice(ROAST_LIST)

async def get_pickup_line() -> str:
    try:
        return random.choice(FLIRT_LIST)
    except Exception as e:
        logger.error(f"❌ Error in get_pickup_line: {str(e)}")
        return "💘 Are you a magician? Because whenever I look at you, everyone else disappears."

async def get_advice() -> str:
    try:
        logger.debug("💡 Getting advice")
        
        # Try advice API with better error handling
        try:
            data = await fetch_api_data(API_ENDPOINTS["advice"], timeout=10)
            if data and isinstance(data, dict) and 'slip' in data:
                slip = data['slip']
                if isinstance(slip, dict) and 'advice' in slip:
                    return f"💡 {slip['advice']}"
        except Exception as e:
            logger.debug(f"⚠️ Advice API failed: {str(e)}")
        
        return random.choice(TIPS_LIST)
        
    except Exception as e:
        logger.error(f"❌ Error in get_advice: {str(e)}")
        return random.choice(TIPS_LIST)

async def get_quote() -> str:
    try:
        logger.debug("✨ Getting quote")
        
        # Try multiple quote APIs
        quote_apis = [
            ("ninja", API_ENDPOINTS["ninja_quotes"]),
            ("quotable", API_ENDPOINTS["quotable"]),
            ("kanye", API_ENDPOINTS["kanye_quotes"])
        ]
        
        for api_name, url in quote_apis:
            try:
                if api_name == "ninja":
                    data = await get_ninja_api_data(url)
                    if data and isinstance(data, list) and len(data) > 0:
                        quote_data = data[0]
                        if isinstance(quote_data, dict) and 'quote' in quote_data and 'author' in quote_data:
                            return f"✨ \"{quote_data['quote']}\" - {quote_data['author']}"
                elif api_name == "quotable":
                    data = await fetch_api_data(url)
                    if data and isinstance(data, dict) and 'content' in data and 'author' in data:
                        return f"✨ \"{data['content']}\" - {data['author']}"
                elif api_name == "kanye":
                    data = await fetch_api_data(url)
                    if data and isinstance(data, dict) and 'quote' in data:
                        return f"🎤 \"{data['quote']}\" - Kanye West"
            except Exception as e:
                logger.debug(f"⚠️ {api_name} API failed: {str(e)}")
                continue
        
        return random.choice(FALLBACK_QUOTES)
        
    except Exception as e:
        logger.error(f"❌ Error in get_quote: {str(e)}")
        return random.choice(FALLBACK_QUOTES)

async def get_compliment() -> str:
    try:
        logger.debug("😊 Getting compliment")
        
        # Try affirmations API
        try:
            data = await fetch_api_data(API_ENDPOINTS["affirmations"])
            if data and isinstance(data, dict) and 'affirmation' in data:
                return f"😊 {data['affirmation']}"
        except Exception as e:
            logger.debug(f"⚠️ Affirmations API failed: {str(e)}")
        
        return random.choice(FALLBACK_COMPLIMENTS)
        
    except Exception as e:
        logger.error(f"❌ Error in get_compliment: {str(e)}")
        return random.choice(FALLBACK_COMPLIMENTS)

async def get_roast() -> str:
    try:
        return random.choice(ROAST_LIST)
    except Exception as e:
        logger.error(f"❌ Error in get_roast: {str(e)}")
        return "😂 You're like a cloud. When you disappear, it's a beautiful day."

async def safe_send_message(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    text: str,
    reply_to_message_id: Optional[int] = None,
    parse_mode: str = ParseMode.HTML,
    disable_web_page_preview: bool = True,
    user_info: Dict[str, Any] = None
) -> bool:
    try:
        if not context or not context.bot or not text or not text.strip():
            return False
            
        if len(text) > 4096:
            text = text[:4090] + "..."
            
        message = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )
        
        log_with_user_info("info", f"✅ Message sent successfully: {message.message_id}", user_info or {})
        return True
        
    except Forbidden as e:
        log_with_user_info("error", f"❌ Bot was blocked or removed from chat: {str(e)}", user_info or {})
        return False
    except BadRequest as e:
        log_with_user_info("error", f"❌ Bad request error: {str(e)}", user_info or {})
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_to_message_id=reply_to_message_id,
                disable_web_page_preview=disable_web_page_preview
            )
            log_with_user_info("info", "✅ Message sent without HTML parsing", user_info or {})
            return True
        except Exception as retry_e:
            log_with_user_info("error", f"❌ Retry failed: {str(retry_e)}", user_info or {})
            return False
    except NetworkError as e:
        log_with_user_info("error", f"❌ Network error: {str(e)}", user_info or {})
        return False
    except TelegramError as e:
        log_with_user_info("error", f"❌ Telegram error: {str(e)}", user_info or {})
        return False
    except Exception as e:
        log_with_user_info("error", f"❌ Unexpected error sending message: {str(e)}", user_info or {})
        return False

async def safe_send_photo(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    photo: str,
    caption: str = None,
    reply_markup: InlineKeyboardMarkup = None,
    parse_mode: str = ParseMode.HTML,
    user_info: Dict[str, Any] = None
) -> bool:
    try:
        if not context or not context.bot or not photo:
            return False
            
        if caption and len(caption) > 1024:
            caption = caption[:1020] + "..."
            
        message = await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
        
        log_with_user_info("info", f"✅ Photo sent successfully: {message.message_id}", user_info or {})
        return True
        
    except Forbidden as e:
        log_with_user_info("error", f"❌ Bot was blocked or removed from chat: {str(e)}", user_info or {})
        return False
    except BadRequest as e:
        log_with_user_info("error", f"❌ Bad request error sending photo: {str(e)}", user_info or {})
        try:
            fallback_text = caption or "Sorry, couldn't send the image!"
            return await safe_send_message(context, chat_id, fallback_text, user_info=user_info)
        except Exception as retry_e:
            log_with_user_info("error", f"❌ Fallback text failed: {str(retry_e)}", user_info or {})
            return False
    except NetworkError as e:
        log_with_user_info("error", f"❌ Network error sending photo: {str(e)}", user_info or {})
        return False
    except TelegramError as e:
        log_with_user_info("error", f"❌ Telegram error sending photo: {str(e)}", user_info or {})
        return False
    except Exception as e:
        log_with_user_info("error", f"❌ Unexpected error sending photo: {str(e)}", user_info or {})
        return False

async def safe_send_chat_action(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    action: ChatAction,
    user_info: Dict[str, Any] = None
) -> bool:
    try:
        if not context or not context.bot:
            return False
            
        await context.bot.send_chat_action(chat_id=chat_id, action=action)
        log_with_user_info("debug", f"✅ Chat action sent: {action}", user_info or {})
        return True
        
    except Exception as e:
        log_with_user_info("warning", f"⚠️ Failed to send chat action: {str(e)}", user_info or {})
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info("🏠 Processing /start command")
        
        if not update or not update.message or not update.message.from_user:
            logger.error("❌ Invalid update object in start command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "🚀 Start command initiated", user_info)
        
        user = update.message.from_user
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        user_mention = user.mention_html() if user.mention_html else user.full_name
        welcome_msg = BOT_MESSAGES["welcome"].format(user=user_mention)
        
        try:
            bot_info = await context.bot.get_me()
            bot_username = bot_info.username if bot_info and bot_info.username else "FlirtyFoxBot"
        except Exception as e:
            logger.warning(f"⚠️ Failed to get bot info: {str(e)}")
            bot_username = "FlirtyFoxBot"

        try:
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
        except Exception as e:
            logger.error(f"❌ Error creating keyboard: {str(e)}")
            reply_markup = None

        try:
            if IMAGES:
                random_image = random.choice(IMAGES)
                success = await safe_send_photo(
                    context, chat_id, random_image, welcome_msg, reply_markup, user_info=user_info
                )
                
                if success:
                    log_with_user_info("info", "✅ Welcome message with image sent successfully", user_info)
                else:
                    await safe_send_message(context, chat_id, welcome_msg, user_info=user_info)
            else:
                await safe_send_message(context, chat_id, welcome_msg, user_info=user_info)
                
        except Exception as e:
            logger.error(f"❌ Error in start command: {str(e)}")
            await safe_send_message(context, chat_id, "👋 Hello! I'm Flirty Fox Bot!", user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Critical error in start command: {str(e)}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info("🏓 Processing /ping command")
        
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "🛰️ Ping command initiated", user_info)
        
        start_time = time.time()
        chat_id = update.effective_chat.id
        
        is_private = update.effective_chat.type == 'private'
        reply_to = None if is_private else update.message.message_id
        
        success = await safe_send_message(
            context, chat_id, BOT_MESSAGES["pinging"], reply_to, user_info=user_info
        )
        
        if not success:
            return
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        pong_message = BOT_MESSAGES["pong"].format(latency=latency)
        await safe_send_message(context, chat_id, pong_message, reply_to, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in ping command: {str(e)}")

async def handle_random_percent(update: Update, context: ContextTypes.DEFAULT_TYPE, label: str):
    try:
        logger.info(f"📊 Processing {label} percentage command")
        
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", f"📊 {label} percentage command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        name, reply_to = get_user_info(update, context)
        
        if not name:
            await safe_send_message(
                context, chat_id, BOT_MESSAGES["provide_name"], user_info=user_info
            )
            return

        percent = random.randint(10, 100)
        feedback = get_feedback(percent)
        
        message = f"{name}, your {label} level is {percent}%\n\n{feedback}"
        
        success = await safe_send_message(
            context, chat_id, message, reply_to, user_info=user_info
        )
        
        if success:
            log_with_user_info("info", f"✅ {label} percentage sent: {percent}%", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in handle_random_percent ({label}): {str(e)}")

async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "love")

async def horny(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "horny")

async def pervy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "pervy")

async def sex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_random_percent(update, context, "sex")

async def facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        fact = await get_random_fact()
        await safe_send_message(context, chat_id, fact, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in facts command: {str(e)}")

async def flirt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        pickup_line = await get_pickup_line()
        await safe_send_message(context, chat_id, pickup_line, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in flirt command: {str(e)}")

async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        advice = await get_advice()
        await safe_send_message(context, chat_id, advice, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in tips command: {str(e)}")

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        quote_text = await get_quote()
        await safe_send_message(context, chat_id, quote_text, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in quote command: {str(e)}")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        joke_text = await get_random_joke()
        await safe_send_message(context, chat_id, joke_text, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in joke command: {str(e)}")

async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        name, reply_to = get_user_info(update, context)
        compliment_text = await get_compliment()
        
        if name:
            message = f"{name}, {compliment_text}"
        else:
            message = compliment_text
        
        await safe_send_message(context, chat_id, message, reply_to, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in compliment command: {str(e)}")

async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        name, reply_to = get_user_info(update, context)
        
        if not name:
            await safe_send_message(
                context, chat_id, BOT_MESSAGES["provide_name"], user_info=user_info
            )
            return

        roast_text = await get_roast()
        message = f"{name}, {roast_text}"
        
        await safe_send_message(context, chat_id, message, reply_to, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in roast command: {str(e)}")

async def t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        msg = random.choice(TRUTHS)
        reply_to = None
        
        if update.message.reply_to_message:
            reply_to = update.message.reply_to_message.message_id
        
        await safe_send_message(context, chat_id, msg, reply_to, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in truth command: {str(e)}")

async def d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        msg = random.choice(DARES)
        reply_to = None
        
        if update.message.reply_to_message:
            reply_to = update.message.reply_to_message.message_id
        
        await safe_send_message(context, chat_id, msg, reply_to, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in dare command: {str(e)}")

async def slap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update or not update.message:
            return
            
        user_info = extract_user_info(update.message)
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        msg = ""
        reply_to = None
        
        if update.message.reply_to_message and update.message.reply_to_message.from_user:
            user = update.message.reply_to_message.from_user
            name = user.mention_html() if user.mention_html else user.full_name
            slap_text = random.choice(SLAPS)
            msg = f"{name}, {slap_text}"
            reply_to = update.message.reply_to_message.message_id
        else:
            msg = random.choice(SLAPS)

        await safe_send_message(context, chat_id, msg, reply_to, user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in slap command: {str(e)}")

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response = b"Flirty Fox Bot is alive and kicking! 🦊💕"
            self.wfile.write(response)
        except Exception as e:
            logger.error(f"❌ Error handling GET request: {str(e)}")
            try:
                self.send_response(500)
                self.end_headers()
            except:
                pass

    def do_HEAD(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
        except Exception as e:
            logger.error(f"❌ Error handling HEAD request: {str(e)}")

    def log_message(self, format, *args):
        message = format % args
        logger.debug(f"🌐 HTTP: {message}")

def start_dummy_server():
    try:
        logger.info(f"🌐 Starting HTTP server on port {PORT}")
        server = HTTPServer(("0.0.0.0", PORT), DummyHandler)
        
        try:
            import socket
            server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except Exception as e:
            logger.warning(f"⚠️ Failed to set socket options: {str(e)}")
        
        logger.info(f"✅ HTTP server listening on port {PORT}")
        server.serve_forever()
        
    except OSError as e:
        if e.errno == 98:
            logger.error(f"❌ Port {PORT} is already in use")
        else:
            logger.error(f"❌ OS error starting server: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Unexpected error starting HTTP server: {str(e)}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        logger.error("❌ Exception while handling an update:")
        logger.error(f"🔍 Context error: {context.error}")
        
        user_info = {}
        if hasattr(update, 'message') and update.message:
            try:
                user_info = extract_user_info(update.message)
            except:
                pass
        
        if hasattr(update, 'effective_chat') and update.effective_chat:
            try:
                await safe_send_message(
                    context, 
                    update.effective_chat.id, 
                    BOT_MESSAGES["error_occurred"],
                    user_info=user_info
                )
            except Exception as e:
                logger.error(f"❌ Failed to send error message to user: {str(e)}")
                
    except Exception as e:
        logger.error(f"❌ Error in error handler: {str(e)}")

def main():
    try:
        logger.info("🚀 Starting Flirty Fox Bot initialization...")
        
        if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("❌ Invalid bot token provided")
            sys.exit(1)
        
        logger.info("🤖 Creating bot application...")
        app = ApplicationBuilder().token(TOKEN).build()
        logger.info("✅ Bot application created successfully")

        app.add_error_handler(error_handler)
        logger.info("✅ Global error handler added")

        logger.info("🎯 Adding command handlers...")
        
        command_handlers = [
            ("start", start),
            ("ping", ping),
            ("love", love),
            ("horny", horny),
            ("pervy", pervy),
            ("sex", sex),
            ("facts", facts),
            ("roast", roast),
            ("flirt", flirt),
            ("tips", tips),
            ("quote", quote),
            ("joke", joke),
            ("compliment", compliment),
            ("t", t),
            ("d", d),
            ("slap", slap),
        ]
        
        for cmd, handler in command_handlers:
            app.add_handler(CommandHandler(cmd, handler))
            logger.debug(f"✅ Added handler for /{cmd}")
        
        logger.info(f"✅ {len(command_handlers)} command handlers added")

        async def post_init(application):
            try:
                logger.info("📋 Setting up bot commands menu...")
                commands = [(cmd, desc) for cmd, desc in COMMANDS.items()]
                await application.bot.set_my_commands(commands)
                logger.info("✅ Bot commands menu has been set up!")
            except Exception as e:
                logger.error(f"❌ Failed to set up commands menu: {str(e)}")
        
        app.post_init = post_init
        
        logger.info("🦊 Flirty Fox Bot is starting...")
        logger.info("🚀 Starting bot polling...")
        
        app.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except KeyboardInterrupt:
        logger.info("⚠️ Bot stopped by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Critical error in main function: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        logger.info("🌟 Flirty Fox Bot starting up...")
        
        logger.info("🌐 Starting HTTP server thread...")
        server_thread = threading.Thread(
            target=start_dummy_server, 
            daemon=True,
            name="HTTPServerThread"
        )
        server_thread.start()
        logger.info("✅ HTTP server thread started")
        
        main()
        
    except Exception as e:
        logger.error(f"❌ Critical startup error: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        sys.exit(1)