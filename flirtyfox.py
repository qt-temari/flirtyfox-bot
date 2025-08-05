import os
import sys
import time
import random
import logging
import asyncio
import aiohttp
import threading
import traceback

from datetime import datetime
from typing import (
    Dict,
    Optional,
    Tuple,
    Any
)
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer
)

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from telegram.constants import (
    ChatAction,
    ParseMode
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from telegram.error import (
    TelegramError,
    NetworkError,
    BadRequest,
    Forbidden
)

# Environment variables configuration
TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
PORT = int(os.environ.get("PORT", 10000))
UPDATES_URL = os.environ.get("UPDATES_URL", "https://t.me/WorkGlows")
SUPPORT_URL = os.environ.get("SUPPORT_URL", "https://t.me/SoulMeetsHQ")
NINJA_API_KEY = os.environ.get("NINJA_API_KEY", "W/cYCzw1s5xXZqRbQafNXA==BxUt1niLMg2M9FgS")
RANDOM_API_TOKEN = os.environ.get("RANDOM_API_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI4MGUyZTVjMS1lMTYzLTQ0ZTAtYTkzZC1iMGJiMGI0ZWQ3OWYiLCJpYXQiOjE3NTQzNzM1NDl9.LTHVkiQTvrY1mRxquFmSfgjcvXR4byhYZQLx77VHuYU")
API_TIMEOUT = int(os.environ.get("API_TIMEOUT", "5"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# API keys dictionary
API_KEYS = {
    "ninja": NINJA_API_KEY,
    "random": RANDOM_API_TOKEN
}

# API endpoints dictionary
API_ENDPOINTS = {
    "ninja_facts": "https://api.api-ninjas.com/v1/facts",
    "ninja_jokes": "https://api.api-ninjas.com/v1/jokes",
    "ninja_quotes": "https://api.api-ninjas.com/v1/quotes",
    "dad_jokes": "https://icanhazdadjoke.com/",
    "pickup_lines": "https://rizzapi.vercel.app/random",
    "advice": "https://api.adviceslip.com/advice",
    "compliments": "https://complimentr.com/api",
    "insults": "https://evilinsult.com/generate_insult.json",
    "cat_facts": "https://catfact.ninja/fact",
    "random_user": "https://randomuser.me/api/"
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

# Romantic fun facts list
FACTS_LIST = [
    "❤️ Kissing can burn up to 6 calories a minute!",
    "💋 Your lips are 100 times more sensitive than your fingertips.",
    "🧠 Falling in love has neurological effects similar to cocaine.",
    "💕 Couples who hold hands have synchronized heartbeats.",
    "🌹 The smell of roses can boost your libido.",
    "😍 Looking into someone's eyes for 4 minutes can make you fall in love.",
    "💘 Chocolate releases the same chemicals as falling in love."
]

# Witty roast messages list
ROAST_LIST = [
    "😂 You're like a cloud. When you disappear, it's a beautiful day.",
    "🔥 I'd roast you, but my mom said I shouldn't burn trash.",
    "😏 You're the reason gene pools need lifeguards.",
    "💀 If laughter is the best medicine, your face must be curing the world.",
    "🎭 You're not stupid; you just have bad luck thinking.",
    "🌟 You're like a shooting star - everyone wishes you'd disappear.",
    "💡 You're so bright, you make the sun jealous... of your stupidity."
]

# Flirty pickup lines list
FLIRT_LIST = [
    "😍 Are you a magician? Because whenever I look at you, everyone else disappears.",
    "🔥 Do you have a map? I keep getting lost in your eyes.",
    "💕 Are you Wi-Fi? Because I'm feeling a connection.",
    "🌟 If you were a vegetable, you'd be a cute-cumber.",
    "💋 Are you made of copper and tellurium? Because you're Cu-Te.",
    "😘 Do you believe in love at first sight, or should I walk by again?",
    "💘 Are you a parking ticket? Because you've got 'fine' written all over you."
]

# Romance dating tips list
TIPS_LIST = [
    "💬 Listen more, talk less - it's sexy.",
    "🔥 Foreplay isn't optional. It's essential.",
    "👁️ Eye contact during conversations increases attraction by 30%.",
    "💋 Light touches on the arm can increase romantic interest.",
    "🌹 Surprise dates are more memorable than expensive ones.",
    "😊 Genuine compliments are more effective than generic ones.",
    "💕 Shared experiences create stronger bonds than material gifts."
]

# Truth game questions list
TRUTHS = [
    "😏 What's your most secret desire?",
    "💋 What's the most romantic thing someone has done for you?",
    "🔥 What's your biggest turn-on?",
    "💕 Have you ever had a crush on someone in this group?",
    "😍 What's the sexiest quality someone can have?",
    "💘 What's your ideal first date?",
    "🌟 What's something you've never told anyone?"
]

# Dare challenge list
DARES = [
    "💌 Send a flirty emoji to the last person you chatted with.",
    "😘 Give someone in the group a virtual kiss.",
    "🔥 Post a story saying 'I'm single and ready to mingle' for 5 minutes.",
    "💋 Send a voice note saying 'Hey gorgeous' to your crush.",
    "😍 Change your profile picture to a selfie with a wink.",
    "💕 Text your ex 'I miss you' then immediately say 'Sorry, wrong person'.",
    "🌹 Compliment the person above you in the most flirty way possible."
]

# Playful slap responses list
SLAPS = [
    "👋 Slaps you with love - don't make me do it again!",
    "🤚 *SLAP* That's for being too cute!",
    "✋ Gets slapped back to reality!",
    "👋 *Slaps gently* Wake up, sunshine!",
    "🤚 Slaps you with a bouquet of roses!",
    "✋ *SLAP* That's what you get for being awesome!",
    "👋 Gets a love slap - the best kind!"
]

# Fallback quotes list
FALLBACK_QUOTES = [
    "✨ \"Love is not about possession, it's about appreciation.\"",
    "💕 \"The best relationships are built on friendship.\"",
    "🌟 \"Be yourself, everyone else is taken.\"",
    "💖 \"Love yourself first, and everything else falls into place.\""
]

# Fallback compliments list
FALLBACK_COMPLIMENTS = [
    "😍 You're absolutely stunning!",
    "✨ Your smile could light up the whole world!",
    "💖 You have such a beautiful soul!",
    "🌟 You're incredibly amazing just the way you are!",
    "💕 Your energy is absolutely contagious!"
]

# Color codes for logging
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class ColoredFormatter(logging.Formatter):
    # Custom formatter colors
    COLORS = {
        'DEBUG': Colors.GREEN,
        'INFO': Colors.YELLOW,
        'WARNING': Colors.BLUE,
        'ERROR': Colors.RED,
    }

    def format(self, record):
        original_format = super().format(record)
        color = self.COLORS.get(record.levelname, Colors.RESET)
        colored_format = f"{color}{original_format}{Colors.RESET}"
        return colored_format

def setup_colored_logging():
    # Setup colored logging
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

# Initialize colored logger
logger = setup_colored_logging()

def extract_user_info(msg: Message) -> Dict[str, any]:
    # Extract user chat information
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
            f"[ID: {info['user_id']}] in {info['chat_title']} [{info['chat_id']}] {info['chat_link']}"
        )
        return info
    except Exception as e:
        logger.error(f"❌ Error extracting user info: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return {}

def log_with_user_info(level: str, message: str, user_info: Dict[str, any]) -> None:
    # Log message with user
    try:
        logger.debug(f"📝 Logging with user info: {level} - {message}")
        
        if not user_info:
            logger.warning("⚠️ No user info provided for logging")
            user_detail = "👤 Unknown User | 💬 Unknown Chat"
        else:
            user_detail = (
                f"👤 {user_info.get('full_name', 'Unknown')} (@{user_info.get('username', 'Unknown')}) "
                f"[ID: {user_info.get('user_id', 'Unknown')}] | "
                f"💬 {user_info.get('chat_title', 'Unknown')} [{user_info.get('chat_id', 'Unknown')}] "
                f"({user_info.get('chat_type', 'Unknown')}) {user_info.get('chat_link', 'Unknown')}"
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
            
        logger.debug(f"✅ Successfully logged message with level: {level}")
    except Exception as e:
        logger.error(f"❌ Error in log_with_user_info: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

def get_feedback(percent: int) -> str:
    # Get feedback message based on percentage
    try:
        logger.debug(f"📊 Getting feedback for percentage: {percent}")
        
        if not isinstance(percent, int):
            logger.warning(f"⚠️ Invalid percentage type: {type(percent)}, converting to int")
            percent = int(percent)
            
        if percent < 0 or percent > 100:
            logger.warning(f"⚠️ Invalid percentage range: {percent}, clamping to 0-100")
            percent = max(0, min(100, percent))
        
        if percent <= 20:
            feedback = FEEDBACK_MESSAGES["low"]
        elif percent <= 40:
            feedback = FEEDBACK_MESSAGES["below_average"]
        elif percent <= 60:
            feedback = FEEDBACK_MESSAGES["average"]
        elif percent <= 80:
            feedback = FEEDBACK_MESSAGES["good"]
        else:
            feedback = FEEDBACK_MESSAGES["excellent"]
            
        logger.debug(f"✅ Feedback generated: {feedback}")
        return feedback
        
    except Exception as e:
        logger.error(f"❌ Error getting feedback: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return "Something's not quite right, but you're awesome anyway!"

def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Tuple[Optional[str], Optional[int]]:
    # Extract user information with error handling
    try:
        logger.debug("🔍 Extracting user info from update")
        
        if not update or not update.message:
            logger.error("❌ Invalid update or message object")
            return None, None
            
        user_info = extract_user_info(update.message)
        log_with_user_info("debug", "📋 Starting user info extraction", user_info)
        
        if update.message.reply_to_message:
            logger.debug("💬 Processing reply message")
            reply_msg = update.message.reply_to_message
            
            if not reply_msg.from_user:
                logger.warning("⚠️ Reply message has no user")
                return None, None
                
            user = reply_msg.from_user
            name = user.mention_html() if user.mention_html else f"@{user.username}" if user.username else user.full_name
            reply_to = reply_msg.message_id
            
            log_with_user_info("info", f"✅ Extracted reply user: {name}", user_info)
            return name, reply_to
            
        elif context and context.args:
            logger.debug("📝 Processing context arguments")
            if not isinstance(context.args, list):
                logger.warning("⚠️ Context args is not a list")
                return None, None
                
            name = " ".join(context.args).strip()
            if not name:
                logger.warning("⚠️ Empty name from context args")
                return None, None
                
            log_with_user_info("info", f"✅ Extracted name from args: {name}", user_info)
            return name, None
        else:
            log_with_user_info("warning", "⚠️ No user info or args provided", user_info)
            return None, None
            
    except Exception as e:
        logger.error(f"❌ Error in get_user_info: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return None, None

async def fetch_api_data(url: str, headers: dict = None, timeout: int = API_TIMEOUT) -> Optional[dict]:
    # Fetch API data with error handling
    try:
        logger.debug(f"🌐 Starting API fetch from: {url}")
        
        if not url:
            logger.error("❌ Empty URL provided")
            return None
            
        if not isinstance(timeout, int) or timeout <= 0:
            logger.warning(f"⚠️ Invalid timeout: {timeout}, using default: {API_TIMEOUT}")
            timeout = API_TIMEOUT
        
        if headers is None:
            headers = {}
        headers.update({
            'User-Agent': 'FlirtyFoxBot/1.0',
            'Accept': 'application/json'
        })
        
        logger.debug(f"📡 Making HTTP request with timeout: {timeout}s")
        
        connector = aiohttp.TCPConnector(limit=10, ttl_dns_cache=300, use_dns_cache=True)
        timeout_config = aiohttp.ClientTimeout(total=timeout, connect=timeout//2)
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout_config,
            headers=headers
        ) as session:
            async with session.get(url) as response:
                logger.debug(f"📊 Response status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ API fetch successful from: {url}")
                    return data
                elif response.status == 429:
                    logger.warning(f"⚠️ Rate limited by API: {url}")
                    return None
                elif response.status == 404:
                    logger.warning(f"⚠️ API endpoint not found: {url}")
                    return None
                elif response.status >= 500:
                    logger.warning(f"⚠️ Server error from API: {url} - Status: {response.status}")
                    return None
                else:
                    logger.warning(f"⚠️ Unexpected status code: {response.status} from {url}")
                    return None
                    
    except asyncio.TimeoutError:
        logger.error(f"⏰ Timeout fetching from: {url}")
        return None
    except aiohttp.ClientError as e:
        logger.error(f"🌐 Client error fetching from {url}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"❌ Unexpected error fetching from {url}: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return None

async def get_ninja_api_data(endpoint: str, category: str = None) -> Optional[dict]:
    # Fetch data from Ninja API
    try:
        logger.debug(f"🥷 Fetching from Ninja API: {endpoint}")
        
        if not endpoint:
            logger.error("❌ Empty endpoint provided for Ninja API")
            return None
            
        if not API_KEYS.get("ninja"):
            logger.error("❌ Ninja API key not available")
            return None
        
        headers = {
            'X-Api-Key': API_KEYS["ninja"],
            'Content-Type': 'application/json'
        }
        
        url = endpoint
        if category:
            url += f"?category={category}"
            logger.debug(f"🏷️ Added category filter: {category}")
        
        logger.debug(f"🔗 Final URL: {url}")
        data = await fetch_api_data(url, headers)
        
        if data:
            logger.info(f"✅ Ninja API fetch successful: {endpoint}")
        else:
            logger.warning(f"⚠️ Ninja API fetch failed: {endpoint}")
            
        return data
        
    except Exception as e:
        logger.error(f"❌ Error in get_ninja_api_data: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return None

async def get_random_fact() -> str:
    # Get random fact with fallbacks
    try:
        logger.debug("🧠 Starting random fact retrieval")
        
        logger.debug("🥷 Trying Ninja API for facts")
        data = await get_ninja_api_data(API_ENDPOINTS["ninja_facts"])
        if data and isinstance(data, list) and len(data) > 0 and 'fact' in data[0]:
            fact = f"🧠 {data[0]['fact']}"
            logger.info("✅ Retrieved fact from Ninja API")
            return fact
        
        logger.debug("⚠️ Ninja API failed, trying Cat Facts API")
        data = await fetch_api_data(API_ENDPOINTS["cat_facts"])
        if data and isinstance(data, dict) and 'fact' in data:
            fact = f"🐱 {data['fact']}"
            logger.info("✅ Retrieved fact from Cat Facts API")
            return fact
        
        logger.warning("⚠️ All APIs failed, using fallback facts")
        fact = random.choice(FACTS_LIST)
        logger.info("✅ Using local fallback fact")
        return fact
        
    except Exception as e:
        logger.error(f"❌ Error in get_random_fact: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return random.choice(FACTS_LIST)

async def get_random_joke() -> str:
    # Get random joke with fallbacks
    try:
        logger.debug("😂 Starting random joke retrieval")
        
        logger.debug("🥷 Trying Ninja API for jokes")
        data = await get_ninja_api_data(API_ENDPOINTS["ninja_jokes"])
        if data and isinstance(data, list) and len(data) > 0 and 'joke' in data[0]:
            joke = f"😂 {data[0]['joke']}"
            logger.info("✅ Retrieved joke from Ninja API")
            return joke
        
        logger.debug("⚠️ Ninja API failed, trying Dad Jokes API")
        headers = {'Accept': 'application/json'}
        data = await fetch_api_data(API_ENDPOINTS["dad_jokes"], headers)
        if data and isinstance(data, dict) and 'joke' in data:
            joke = f"👨‍💼 {data['joke']}"
            logger.info("✅ Retrieved joke from Dad Jokes API")
            return joke
        
        logger.warning("⚠️ All APIs failed, using fallback roasts as jokes")
        joke = random.choice(ROAST_LIST)
        logger.info("✅ Using local fallback roast as joke")
        return joke
        
    except Exception as e:
        logger.error(f"❌ Error in get_random_joke: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return random.choice(ROAST_LIST)

async def get_pickup_line() -> str:
    # Get pickup line with fallbacks
    try:
        logger.debug("💘 Starting pickup line retrieval")
        
        logger.debug("🔥 Trying Rizz API for pickup lines")
        data = await fetch_api_data(API_ENDPOINTS["pickup_lines"])
        if data and isinstance(data, dict) and 'text' in data:
            line = f"💘 {data['text']}"
            logger.info("✅ Retrieved pickup line from Rizz API")
            return line
        
        logger.warning("⚠️ API failed, using fallback pickup lines")
        line = random.choice(FLIRT_LIST)
        logger.info("✅ Using local fallback pickup line")
        return line
        
    except Exception as e:
        logger.error(f"❌ Error in get_pickup_line: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return random.choice(FLIRT_LIST)

async def get_advice() -> str:
    # Get advice with fallbacks
    try:
        logger.debug("💡 Starting advice retrieval")
        
        logger.debug("🎯 Trying Advice Slip API")
        data = await fetch_api_data(API_ENDPOINTS["advice"])
        if data and isinstance(data, dict) and 'slip' in data and isinstance(data['slip'], dict) and 'advice' in data['slip']:
            advice = f"💡 {data['slip']['advice']}"
            logger.info("✅ Retrieved advice from Advice Slip API")
            return advice
        
        logger.warning("⚠️ API failed, using fallback tips")
        advice = random.choice(TIPS_LIST)
        logger.info("✅ Using local fallback tip")
        return advice
        
    except Exception as e:
        logger.error(f"❌ Error in get_advice: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return random.choice(TIPS_LIST)

async def get_quote() -> str:
    # Get inspirational quote with fallbacks
    try:
        logger.debug("✨ Starting quote retrieval")
        
        logger.debug("🥷 Trying Ninja API for quotes")
        data = await get_ninja_api_data(API_ENDPOINTS["ninja_quotes"])
        if data and isinstance(data, list) and len(data) > 0:
            quote_data = data[0]
            if isinstance(quote_data, dict) and 'quote' in quote_data and 'author' in quote_data:
                quote = f"✨ \"{quote_data['quote']}\" - {quote_data['author']}"
                logger.info("✅ Retrieved quote from Ninja API")
                return quote
        
        logger.warning("⚠️ API failed, using fallback quotes")
        quote = random.choice(FALLBACK_QUOTES)
        logger.info("✅ Using local fallback quote")
        return quote
        
    except Exception as e:
        logger.error(f"❌ Error in get_quote: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return random.choice(FALLBACK_QUOTES)

async def get_compliment() -> str:
    # Get compliment with fallbacks
    try:
        logger.debug("😊 Starting compliment retrieval")
        
        logger.debug("💖 Trying Complimentr API")
        data = await fetch_api_data(API_ENDPOINTS["compliments"])
        if data and isinstance(data, dict) and 'compliment' in data:
            compliment = f"😊 {data['compliment']}"
            logger.info("✅ Retrieved compliment from Complimentr API")
            return compliment
        
        logger.warning("⚠️ API failed, using fallback compliments")
        compliment = random.choice(FALLBACK_COMPLIMENTS)
        logger.info("✅ Using local fallback compliment")
        return compliment
        
    except Exception as e:
        logger.error(f"❌ Error in get_compliment: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return random.choice(FALLBACK_COMPLIMENTS)

async def get_roast() -> str:
    # Get roast with fallbacks
    try:
        logger.debug("🔥 Starting roast retrieval")
        
        logger.debug("😈 Trying Evil Insult API")
        data = await fetch_api_data(API_ENDPOINTS["insults"])
        if data and isinstance(data, dict) and 'insult' in data:
            roast = f"🔥 {data['insult']}"
            logger.info("✅ Retrieved roast from Evil Insult API")
            return roast
        
        logger.warning("⚠️ API failed, using fallback roasts")
        roast = random.choice(ROAST_LIST)
        logger.info("✅ Using local fallback roast")
        return roast
        
    except Exception as e:
        logger.error(f"❌ Error in get_roast: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return random.choice(ROAST_LIST)

async def safe_send_message(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    text: str,
    reply_to_message_id: Optional[int] = None,
    parse_mode: str = ParseMode.HTML,
    disable_web_page_preview: bool = True,
    user_info: Dict[str, Any] = None
) -> bool:
    # Safely send message with error handling
    try:
        logger.debug(f"📤 Attempting to send message to chat {chat_id}")
        
        if not context or not context.bot:
            logger.error("❌ Invalid context or bot object")
            return False
            
        if not text or not text.strip():
            logger.error("❌ Empty message text provided")
            return False
            
        if len(text) > 4096:
            logger.warning(f"⚠️ Message too long ({len(text)} chars), truncating")
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
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
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
    # Safely send photo with error handling
    try:
        logger.debug(f"📷 Attempting to send photo to chat {chat_id}")
        
        if not context or not context.bot:
            logger.error("❌ Invalid context or bot object")
            return False
            
        if not photo:
            logger.error("❌ Empty photo URL provided")
            return False
            
        if caption and len(caption) > 1024:
            logger.warning(f"⚠️ Caption too long ({len(caption)} chars), truncating")
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
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        return False

async def safe_send_chat_action(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    action: ChatAction,
    user_info: Dict[str, Any] = None
) -> bool:
    # Safely send chat action
    try:
        logger.debug(f"⚡ Sending chat action: {action}")
        
        if not context or not context.bot:
            logger.error("❌ Invalid context or bot object")
            return False
            
        await context.bot.send_chat_action(chat_id=chat_id, action=action)
        log_with_user_info("debug", f"✅ Chat action sent: {action}", user_info or {})
        return True
        
    except Exception as e:
        log_with_user_info("warning", f"⚠️ Failed to send chat action: {str(e)}", user_info or {})
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle start command
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
            logger.debug(f"🤖 Bot username: {bot_username}")
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
            logger.debug("✅ Keyboard created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating keyboard: {str(e)}")
            reply_markup = None

        try:
            if IMAGES:
                random_image = random.choice(IMAGES)
                logger.debug(f"🖼️ Selected random image: {random_image}")
                
                success = await safe_send_photo(
                    context, chat_id, random_image, welcome_msg, reply_markup, user_info=user_info
                )
                
                if success:
                    log_with_user_info("info", "✅ Welcome message with image sent successfully", user_info)
                else:
                    logger.warning("⚠️ Image failed, sending text message")
                    await safe_send_message(context, chat_id, welcome_msg, user_info=user_info)
            else:
                logger.warning("⚠️ No images available, sending text message")
                await safe_send_message(context, chat_id, welcome_msg, user_info=user_info)
                
        except Exception as e:
            logger.error(f"❌ Error in start command: {str(e)}")
            logger.error(f"🔍 Traceback: {traceback.format_exc()}")
            await safe_send_message(context, chat_id, "👋 Hello! I'm Flirty Fox Bot!", user_info=user_info)
            
    except Exception as e:
        logger.error(f"❌ Critical error in start command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        start_time = time.time()
        
        # Send initial ping message (reply in groups, normal in private)
        reply_to = update.message.message_id if update.effective_chat.type != 'private' else None
        
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=BOT_MESSAGES["pinging"],
            reply_to_message_id=reply_to
        )
        
        # Calculate latency and edit the message
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            text=BOT_MESSAGES["pong"].format(latency=latency),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        logger.error(f"Error in ping command: {e}")

async def handle_random_percent(update: Update, context: ContextTypes.DEFAULT_TYPE, label: str):
    # Handle percentage based commands
    try:
        logger.info(f"📊 Processing {label} percentage command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in percentage command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", f"📊 {label} percentage command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        name, reply_to = get_user_info(update, context)
        
        if not name:
            log_with_user_info("warning", "⚠️ No name provided for percentage command", user_info)
            await safe_send_message(
                context, chat_id, BOT_MESSAGES["provide_name"], user_info=user_info
            )
            return

        try:
            percent = random.randint(10, 100)
            feedback = get_feedback(percent)
            logger.debug(f"🎲 Generated {label} percentage: {percent}% with feedback: {feedback}")
        except Exception as e:
            logger.error(f"❌ Error generating percentage: {str(e)}")
            percent = 50
            feedback = "Something's not quite right, but you're awesome anyway!"
        
        message = f"{name}, your {label} level is {percent}%\n\n{feedback}"
        
        success = await safe_send_message(
            context, chat_id, message, reply_to, user_info=user_info
        )
        
        if success:
            log_with_user_info("info", f"✅ {label} percentage sent: {percent}%", user_info)
        else:
            log_with_user_info("error", f"❌ Failed to send {label} percentage", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in handle_random_percent ({label}): {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle love command
    try:
        await handle_random_percent(update, context, "love")
    except Exception as e:
        logger.error(f"❌ Error in love command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def horny(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle horny command
    try:
        await handle_random_percent(update, context, "horny")
    except Exception as e:
        logger.error(f"❌ Error in horny command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def pervy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle pervy command
    try:
        await handle_random_percent(update, context, "pervy")
    except Exception as e:
        logger.error(f"❌ Error in pervy command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def sex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle sex command
    try:
        await handle_random_percent(update, context, "sex")
    except Exception as e:
        logger.error(f"❌ Error in sex command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle facts command
    try:
        logger.info("🧠 Processing /facts command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in facts command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "🧠 Facts command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        fact = await get_random_fact()
        
        success = await safe_send_message(context, chat_id, fact, user_info=user_info)
        
        if success:
            log_with_user_info("info", "✅ Fact sent successfully", user_info)
        else:
            log_with_user_info("error", "❌ Failed to send fact", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in facts command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def flirt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle flirt command
    try:
        logger.info("💘 Processing /flirt command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in flirt command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "💘 Flirt command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        pickup_line = await get_pickup_line()
        
        success = await safe_send_message(context, chat_id, pickup_line, user_info=user_info)
        
        if success:
            log_with_user_info("info", "✅ Pickup line sent successfully", user_info)
        else:
            log_with_user_info("error", "❌ Failed to send pickup line", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in flirt command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle tips command
    try:
        logger.info("💡 Processing /tips command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in tips command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "💡 Tips command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        advice = await get_advice()
        
        success = await safe_send_message(context, chat_id, advice, user_info=user_info)
        
        if success:
            log_with_user_info("info", "✅ Advice sent successfully", user_info)
        else:
            log_with_user_info("error", "❌ Failed to send advice", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in tips command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle quote command
    try:
        logger.info("✨ Processing /quote command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in quote command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "✨ Quote command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        quote_text = await get_quote()
        
        success = await safe_send_message(context, chat_id, quote_text, user_info=user_info)
        
        if success:
            log_with_user_info("info", "✅ Quote sent successfully", user_info)
        else:
            log_with_user_info("error", "❌ Failed to send quote", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in quote command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle joke command
    try:
        logger.info("😂 Processing /joke command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in joke command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "😂 Joke command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        joke_text = await get_random_joke()
        
        success = await safe_send_message(context, chat_id, joke_text, user_info=user_info)
        
        if success:
            log_with_user_info("info", "✅ Joke sent successfully", user_info)
        else:
            log_with_user_info("error", "❌ Failed to send joke", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in joke command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle compliment command
    try:
        logger.info("😊 Processing /compliment command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in compliment command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "😊 Compliment command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        name, reply_to = get_user_info(update, context)
        
        compliment_text = await get_compliment()
        
        if name:
            message = f"{name}, {compliment_text}"
            log_with_user_info("debug", f"🎯 Compliment targeted to: {name}", user_info)
        else:
            message = compliment_text
            log_with_user_info("debug", "🎯 General compliment", user_info)
        
        success = await safe_send_message(
            context, chat_id, message, reply_to, user_info=user_info
        )
        
        if success:
            log_with_user_info("info", "✅ Compliment sent successfully", user_info)
        else:
            log_with_user_info("error", "❌ Failed to send compliment", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in compliment command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle roast command
    try:
        logger.info("🔥 Processing /roast command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in roast command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "🔥 Roast command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        name, reply_to = get_user_info(update, context)
        
        if not name:
            log_with_user_info("warning", "⚠️ No name provided for roast command", user_info)
            await safe_send_message(
                context, chat_id, BOT_MESSAGES["provide_name"], user_info=user_info
            )
            return

        roast_text = await get_roast()
        message = f"{name}, {roast_text}"
        
        success = await safe_send_message(
            context, chat_id, message, reply_to, user_info=user_info
        )
        
        if success:
            log_with_user_info("info", f"✅ Roast sent to: {name}", user_info)
        else:
            log_with_user_info("error", "❌ Failed to send roast", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in roast command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle truth command
    try:
        logger.info("❓ Processing /t (truth) command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in truth command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "❓ Truth command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        try:
            msg = random.choice(TRUTHS)
            logger.debug(f"🎲 Selected truth: {msg}")
        except Exception as e:
            logger.error(f"❌ Error selecting truth: {str(e)}")
            msg = "😏 What's your most secret desire?"
        
        reply_to = None
        try:
            if update.message.reply_to_message:
                reply_to = update.message.reply_to_message.message_id
                logger.debug(f"💬 Replying to message: {reply_to}")
        except Exception as e:
            logger.warning(f"⚠️ Error getting reply info: {str(e)}")
        
        success = await safe_send_message(
            context, chat_id, msg, reply_to, user_info=user_info
        )
        
        if success:
            log_with_user_info("info", "✅ Truth question sent successfully", user_info)
        else:
            log_with_user_info("error", "❌ Failed to send truth question", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in truth command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle dare command
    try:
        logger.info("🎲 Processing /d (dare) command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in dare command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "🎲 Dare command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        try:
            msg = random.choice(DARES)
            logger.debug(f"🎲 Selected dare: {msg}")
        except Exception as e:
            logger.error(f"❌ Error selecting dare: {str(e)}")
            msg = "💌 Send a flirty emoji to the last person you chatted with."
        
        reply_to = None
        try:
            if update.message.reply_to_message:
                reply_to = update.message.reply_to_message.message_id
                logger.debug(f"💬 Replying to message: {reply_to}")
        except Exception as e:
            logger.warning(f"⚠️ Error getting reply info: {str(e)}")
        
        success = await safe_send_message(
            context, chat_id, msg, reply_to, user_info=user_info
        )
        
        if success:
            log_with_user_info("info", "✅ Dare challenge sent successfully", user_info)
        else:
            log_with_user_info("error", "❌ Failed to send dare challenge", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in dare command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def slap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle slap command
    try:
        logger.info("👋 Processing /slap command")
        
        if not update or not update.message:
            logger.error("❌ Invalid update object in slap command")
            return
            
        user_info = extract_user_info(update.message)
        log_with_user_info("info", "👋 Slap command initiated", user_info)
        
        chat_id = update.effective_chat.id
        
        await safe_send_chat_action(context, chat_id, ChatAction.TYPING, user_info)
        
        msg = ""
        reply_to = None
        
        try:
            if update.message.reply_to_message and update.message.reply_to_message.from_user:
                user = update.message.reply_to_message.from_user
                name = user.mention_html() if user.mention_html else user.full_name
                slap_text = random.choice(SLAPS)
                msg = f"{name}, {slap_text}"
                reply_to = update.message.reply_to_message.message_id
                log_with_user_info("debug", f"🎯 Slapping user: {name}", user_info)
            else:
                msg = random.choice(SLAPS)
                log_with_user_info("debug", "🎯 General slap", user_info)
                
        except Exception as e:
            logger.error(f"❌ Error processing slap target: {str(e)}")
            msg = random.choice(SLAPS)

        success = await safe_send_message(
            context, chat_id, msg, reply_to, user_info=user_info
        )
        
        if success:
            log_with_user_info("info", "✅ Slap sent successfully", user_info)
        else:
            log_with_user_info("error", "❌ Failed to send slap", user_info)
            
    except Exception as e:
        logger.error(f"❌ Error in slap command: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

class DummyHandler(BaseHTTPRequestHandler):
    # HTTP request handler
    
    def do_GET(self):
        # Handle GET requests
        try:
            logger.debug("🌐 Handling GET request")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response = b"Flirty Fox Bot is alive!"
            self.wfile.write(response)
            logger.debug("✅ GET request handled successfully")
        except Exception as e:
            logger.error(f"❌ Error handling GET request: {str(e)}")
            try:
                self.send_response(500)
                self.end_headers()
            except:
                pass

    def do_HEAD(self):
        # Handle HEAD requests
        try:
            logger.debug("🌐 Handling HEAD request")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            logger.debug("✅ HEAD request handled successfully")
        except Exception as e:
            logger.error(f"❌ Error handling HEAD request: {str(e)}")
            try:
                self.send_response(500)
                self.end_headers()
            except:
                pass

    def log_message(self, format, *args):
        # Override log_message
        try:
            message = format % args
            logger.debug(f"🌐 HTTP: {message}")
        except Exception as e:
            logger.error(f"❌ Error logging HTTP message: {str(e)}")

def start_dummy_server():
    # Start HTTP server
    try:
        logger.info(f"🌐 Starting HTTP server on port {PORT}")
        
        server = HTTPServer(("0.0.0.0", PORT), DummyHandler)
        logger.info(f"✅ HTTP server listening on port {PORT}")
        
        try:
            import socket
            server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            logger.debug("✅ Socket options set")
        except Exception as e:
            logger.warning(f"⚠️ Failed to set socket options: {str(e)}")
        
        server.serve_forever()
        
    except OSError as e:
        if e.errno == 98:
            logger.error(f"❌ Port {PORT} is already in use")
        else:
            logger.error(f"❌ OS error starting server: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Unexpected error starting HTTP server: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Global error handler
    try:
        logger.error("❌ Exception while handling an update:")
        logger.error(f"🔍 Update: {update}")
        logger.error(f"🔍 Context error: {context.error}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        
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
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")

def main():
    # Main bot function
    try:
        logger.info("🚀 Starting Flirty Fox Bot initialization...")
        
        if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("❌ Invalid bot token provided")
            sys.exit(1)
        
        logger.info("🤖 Creating bot application...")
        
        try:
            app = ApplicationBuilder().token(TOKEN).build()
            logger.info("✅ Bot application created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create bot application: {str(e)}")
            logger.error(f"🔍 Traceback: {traceback.format_exc()}")
            sys.exit(1)

        try:
            app.add_error_handler(error_handler)
            logger.info("✅ Global error handler added")
        except Exception as e:
            logger.error(f"❌ Failed to add error handler: {str(e)}")

        try:
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
                try:
                    app.add_handler(CommandHandler(cmd, handler))
                    logger.debug(f"✅ Added handler for /{cmd}")
                except Exception as e:
                    logger.error(f"❌ Failed to add handler for /{cmd}: {str(e)}")
            
            logger.info(f"✅ {len(command_handlers)} command handlers added")
            
        except Exception as e:
            logger.error(f"❌ Error adding command handlers: {str(e)}")
            logger.error(f"🔍 Traceback: {traceback.format_exc()}")

        logger.info("🦊 Flirty Fox Bot is starting...")
        
        async def post_init(application):
            # Post initialization setup
            try:
                logger.info("📋 Setting up bot commands menu...")
                commands = [(cmd, desc) for cmd, desc in COMMANDS.items()]
                await application.bot.set_my_commands(commands)
                logger.info("✅ Bot commands menu has been set up!")
            except Exception as e:
                logger.error(f"❌ Failed to set up commands menu: {str(e)}")
                logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        
        try:
            app.post_init = post_init
            logger.debug("✅ Post-init function set")
        except Exception as e:
            logger.error(f"❌ Failed to set post-init function: {str(e)}")
        
        try:
            logger.info("🚀 Starting bot polling...")
            app.run_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )
        except Exception as e:
            logger.error(f"❌ Error running bot: {str(e)}")
            logger.error(f"🔍 Traceback: {traceback.format_exc()}")
            sys.exit(1)
            
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
        
        try:
            logger.info("🌐 Starting HTTP server thread...")
            server_thread = threading.Thread(
                target=start_dummy_server, 
                daemon=True,
                name="HTTPServerThread"
            )
            server_thread.start()
            logger.info("✅ HTTP server thread started")
        except Exception as e:
            logger.error(f"❌ Failed to start HTTP server thread: {str(e)}")
            logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        
        main()
        
    except Exception as e:
        logger.error(f"❌ Critical startup error: {str(e)}")
        logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        sys.exit(1)