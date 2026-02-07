# VedicDose Video Automation Guide for Cheenu

**Purpose:** This document provides step-by-step instructions for Cheenu to automatically create and post VedicDose Instagram Reels daily.

**Security:** All API keys must be stored in `.env` file (NOT in Git). See SECURITY.md for details.

---

## 📋 OVERVIEW

**Daily Workflow:**
1. Determine today's content type (Rasi/Nakshatra/Transit/Tip)
2. Generate video using Python script
3. Post to Instagram @vedic.dose
4. Log success/failure

**Frequency:** Once daily at 7:00 AM IST
**Duration:** 30 seconds per video
**Format:** 1080x1920 MP4 (Instagram Reel)

---

## 🔧 TECHNICAL REQUIREMENTS

### Software Dependencies
```bash
# Install required Python packages
pip install --break-system-packages pillow numpy moviepy instagrapi python-dotenv
```

### Required Files
- `video_generator.py` - Main video creation script
- `content_calendar.json` - 30-day content rotation
- `instagram_poster.py` - Instagram API posting script
- `.env` - API keys (NEVER commit to Git)
- `.env.example` - Template showing required variables

### Environment Variables (in .env file)
```
INSTAGRAM_USERNAME=vedic.dose
INSTAGRAM_PASSWORD=your_password_here
INSTAGRAM_SESSION_FILE=./session.json
```

---

## 📅 CONTENT CALENDAR LOGIC

**30-Day Rotation:**

### Week 1: Fire Signs
- Day 1: Aries (Mesha)
- Day 2: Leo (Simha) 
- Day 3: Sagittarius (Dhanu)

### Week 2: Earth Signs
- Day 4: Taurus (Vrishabha)
- Day 5: Virgo (Kanya)
- Day 6: Capricorn (Makara)

### Week 3: Air Signs
- Day 7: Gemini (Mithuna)
- Day 8: Libra (Tula)
- Day 9: Aquarius (Kumbha)

### Week 4: Water Signs
- Day 10: Cancer (Karkataka)
- Day 11: Scorpio (Vrishchika)
- Day 12: Pisces (Meena)

**Days 13-27:** Nakshatra deep dives (Ashwini through Revati)
**Days 28-30:** Quick tips & remedies

**Formula:** `day_of_month % 30` determines content type

---

## 🎬 VIDEO GENERATION STEPS

### Step 1: Determine Today's Content

```python
import datetime
import json

# Get today's day of month (1-30)
day = datetime.datetime.now().day % 30
if day == 0:
    day = 30

# Load content calendar
with open('content_calendar.json', 'r') as f:
    calendar = json.load(f)

content = calendar[str(day)]
# content = {
#     "type": "rasi",  # or "nakshatra", "transit", "tip"
#     "title_english": "TAURUS",
#     "title_devanagari": "वृषभ राशि",
#     "subtitle": "Vrishabha Rasi",
#     "traits": ["Stable & Patient", "Venus Blessed", "Creative Soul"],
#     "symbol_type": "taurus"  # for drawing the symbol
# }
```

### Step 2: Generate Video

**Execute video generator:**
```bash
python3 video_generator.py --content-day $DAY
```

**What the script does:**
1. Creates 1080x1920 background (navy #0a0a1f)
2. Draws mandala pattern overlay
3. Adds zodiac/nakshatra symbol (gold #d4af37)
4. Renders Devanagari text
5. Adds English title and traits
6. Applies rangoli-style decorations
7. Animates text (fade-in effects)
8. Adds 432 Hz ambient audio
9. Exports as MP4

**Output:** `./output/VedicDose_[Date]_[Content].mp4`

### Step 3: Generate Caption

**Caption Template:**
```python
caption_templates = {
    "rasi": """Think {rasi} is just {stereotype}? Think again! {emoji}

{devanagari_name} - {tagline}

{rasi} natives are:
{trait_1}
{trait_2}
{trait_3}

Are you a {rasi}? Drop {emoji} below!

Follow @vedic.dose for your daily dose of Vedic wisdom 🌟

{hashtags}""",
    
    "nakshatra": """Born under {nakshatra} Nakshatra? Here's your cosmic truth ✨

{devanagari_name}

{characteristic_1}
{characteristic_2}
{characteristic_3}

Compatible: {compatible_nakshatras}

Follow @vedic.dose for daily Vedic wisdom 🌙

{hashtags}""",
    
    "transit": """TODAY'S COSMIC ENERGY 🌟
{date}

✅ DO:
{do_1}
{do_2}
{do_3}

❌ AVOID:
{avoid_1}
{avoid_2}

⏰ Best Time: {best_time}

Follow @vedic.dose for daily guidance 🕉️

{hashtags}""",
    
    "tip": """VEDIC WISDOM OF THE DAY 💫

{tip_main}

{tip_explanation}

Try this today and watch the shift! ✨

Follow @vedic.dose for daily Vedic hacks 🌟

{hashtags}"""
}

# Base hashtags (always include)
base_hashtags = "#VedicAstrology #Jyotish #VedicDose #VedicWisdom #HinduAstrology #IndianAstrology #AstrologyReels #Horoscope"

# Content-specific hashtags
rasi_hashtags = "#ZodiacSigns #AstrologyDaily #RasiPalan"
nakshatra_hashtags = "#Nakshatra #BirthStar #VedicHoroscope"
transit_hashtags = "#DailyHoroscope #CosmicEnergy #Panchang"
tip_hashtags = "#VedicTips #SpiritualGrowth #AncientWisdom"
```

### Step 4: Post to Instagram

**Execute poster script:**
```bash
python3 instagram_poster.py --video ./output/[filename].mp4 --caption-file ./output/caption.txt
```

**What the script does:**
1. Loads Instagram credentials from `.env`
2. Authenticates using saved session (or creates new)
3. Uploads video as Reel
4. Adds caption with hashtags
5. Sets cover image (frame at 3 seconds)
6. Shares to feed
7. Logs success/failure

**Output:** Log entry in `posting_log.json`

---

## 🔐 SECURITY REQUIREMENTS

### .env File (NEVER COMMIT)
```bash
# Instagram Credentials
INSTAGRAM_USERNAME=vedic.dose
INSTAGRAM_PASSWORD=your_secure_password

# Session Management
INSTAGRAM_SESSION_FILE=./session.json

# Optional: Gemini API for dynamic content
GEMINI_API_KEY=your_gemini_key_here
```

### .gitignore (MUST INCLUDE)
```
.env
.env.*
*.key
*_SECRET*
session.json
*.session
credentials.json
config.json
__pycache__/
*.pyc
.DS_Store
output/*.mp4
logs/*.log
```

### Session Management
- Instagram session is saved in `session.json` after first login
- Reuses session to avoid repeated logins (prevents security flags)
- Session expires after ~90 days, will auto-regenerate

---

## 📂 FILE STRUCTURE

```
vedicdose/
├── .env                      # API keys (NOT in Git)
├── .env.example             # Template for .env
├── .gitignore               # Security exclusions
├── README.md                # Project overview
├── AUTOMATION_GUIDE.md      # This file
├── SECURITY.md              # Security protocols
├── requirements.txt         # Python dependencies
├── content_calendar.json    # 30-day content rotation
├── scripts/
│   ├── video_generator.py   # Main video creation
│   ├── instagram_poster.py  # Instagram API posting
│   ├── caption_generator.py # Dynamic captions
│   └── content_selector.py  # Daily content logic
├── templates/
│   ├── rasi_template.py     # Zodiac sign videos
│   ├── nakshatra_template.py # Birth star videos
│   ├── transit_template.py  # Daily transit videos
│   └── tip_template.py      # Quick tips videos
├── data/
│   ├── rasi_data.json       # 12 zodiac signs data
│   ├── nakshatra_data.json  # 27 nakshatras data
│   └── tips_data.json       # Vedic tips collection
├── output/                  # Generated videos (gitignored)
├── logs/                    # Execution logs (gitignored)
└── session.json            # Instagram session (gitignored)
```

---

## 🤖 AUTOMATION EXECUTION

### Method 1: Make.com Scheduler (Recommended)

**Setup Steps:**
1. Create Make.com account (free tier)
2. New Scenario → Add "Schedule" trigger
3. Set time: 7:00 AM IST daily
4. Add "Webhook" action → Call your server
5. Webhook executes: `python3 automation_master.py`

**automation_master.py does:**
```python
# 1. Determine today's content
# 2. Generate video
# 3. Generate caption
# 4. Post to Instagram
# 5. Log result
# 6. Send Slack notification (optional)
```

### Method 2: Cron Job (Linux/Mac)

**Add to crontab:**
```bash
# Run daily at 7:00 AM IST (1:30 AM UTC)
30 1 * * * cd /path/to/vedicdose && /usr/bin/python3 automation_master.py >> logs/cron.log 2>&1
```

### Method 3: Manual Execution (Testing)

```bash
cd /path/to/vedicdose
python3 automation_master.py
```

---

## 📊 EXECUTION WORKFLOW

### automation_master.py Logic

```python
#!/usr/bin/env python3
"""
VedicDose Automation Master Script
Runs daily to create and post Instagram Reel
"""

import os
import sys
import json
import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    filename='logs/automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    try:
        # Step 1: Determine today's content
        logging.info("Step 1: Determining today's content...")
        from scripts.content_selector import get_today_content
        content = get_today_content()
        logging.info(f"Content: {content['type']} - {content['title_english']}")
        
        # Step 2: Generate video
        logging.info("Step 2: Generating video...")
        from scripts.video_generator import create_video
        video_path = create_video(content)
        logging.info(f"Video created: {video_path}")
        
        # Step 3: Generate caption
        logging.info("Step 3: Generating caption...")
        from scripts.caption_generator import generate_caption
        caption = generate_caption(content)
        
        # Step 4: Post to Instagram
        logging.info("Step 4: Posting to Instagram...")
        from scripts.instagram_poster import post_to_instagram
        post_result = post_to_instagram(video_path, caption)
        
        if post_result['success']:
            logging.info(f"✅ SUCCESS! Post URL: {post_result['url']}")
            print("✅ Video posted successfully!")
            
            # Optional: Send notification
            send_success_notification(post_result)
        else:
            logging.error(f"❌ FAILED: {post_result['error']}")
            print(f"❌ Posting failed: {post_result['error']}")
            
            # Optional: Send alert
            send_failure_alert(post_result['error'])
        
        return 0
        
    except Exception as e:
        logging.error(f"❌ CRITICAL ERROR: {str(e)}", exc_info=True)
        print(f"❌ Critical error: {str(e)}")
        send_failure_alert(str(e))
        return 1

def send_success_notification(result):
    """Send Slack/Email notification on success"""
    # Implementation optional
    pass

def send_failure_alert(error):
    """Send alert on failure"""
    # Implementation optional
    pass

if __name__ == "__main__":
    sys.exit(main())
```

---

## 🎨 VIDEO GENERATION DETAILS

### Design Specifications

**Background:**
- Base color: Navy #0a0a1f
- Mandala overlay: Concentric circles, 15-20% opacity gold
- Decorative dots: Rangoli-style at circle intersections

**Text Elements:**
- Devanagari title: 60px, gold, with saffron glow
- English title: 120px, Montserrat Bold, gold
- Subtitle: 55px, saffron #ff9933
- Traits: 70px, white, with 3px shadow
- Watermark: @vedic.dose, 50px, gold, 60% opacity

**Zodiac/Nakshatra Symbol:**
- Position: Left 1/4 of screen
- Size: 400x400px
- Style: Line art with decorative elements
- Color: Gold with 40% transparency
- Rangoli patterns around perimeter

**Decorative Elements:**
- Top border: Triangular rangoli pattern
- Bottom border: Matching triangular pattern
- Corner accents: Small mandala motifs
- Bullet points: Lotus/rangoli style (not plain dots)

**Animation Timeline:**
- 0-3s: Symbol fade in
- 1-4s: Devanagari title fade in
- 2-5s: English title fade in
- 4-10s: Traits appear (staggered)
- 10-30s: Hold full content

**Audio:**
- 432 Hz sine wave (sacred Vedic frequency)
- Volume: 60-70%
- Duration: 30 seconds
- Alternative: Upload Indian classical instrumental from YouTube Audio Library

---

## 📝 CONTENT DATA FORMAT

### content_calendar.json Structure

```json
{
  "1": {
    "type": "rasi",
    "title_english": "ARIES",
    "title_devanagari": "मेष राशि",
    "subtitle": "Mesha Rasi",
    "traits": [
      "Bold & Courageous",
      "Mars Powered",
      "Natural Leader"
    ],
    "symbol_type": "aries",
    "emoji": "♈",
    "stereotype": "impulsive",
    "tagline": "The Warrior Spirit",
    "hashtags": "#Aries #MeshaRasi"
  },
  "4": {
    "type": "rasi",
    "title_english": "TAURUS",
    "title_devanagari": "वृषभ राशि",
    "subtitle": "Vrishabha Rasi",
    "traits": [
      "Stable & Patient",
      "Venus Blessed",
      "Creative Soul"
    ],
    "symbol_type": "taurus",
    "emoji": "♉",
    "stereotype": "stubborn",
    "tagline": "The Venus Blessed",
    "hashtags": "#Taurus #VrishabhRasi"
  },
  "13": {
    "type": "nakshatra",
    "title_english": "ASHWINI",
    "title_devanagari": "अश्विनी नक्षत्र",
    "subtitle": "Ashwini Nakshatra",
    "traits": [
      "Swift & Energetic",
      "Healing Powers",
      "New Beginnings"
    ],
    "symbol_type": "ashwini",
    "deity": "Ashwini Kumaras",
    "planet": "Ketu",
    "compatible": "Bharani, Krittika",
    "hashtags": "#Ashwini #AshwiniNakshatra"
  },
  "28": {
    "type": "tip",
    "title_english": "CHANT 'OM' FACING EAST",
    "tip_main": "Chant 'OM' facing East for mental clarity",
    "tip_explanation": "Ancient Vedic practice for focus & peace",
    "icon": "🕉️",
    "best_time": "Early morning (5-7 AM)",
    "hashtags": "#VedicTips #MorningRituals"
  }
}
```

---

## 🔍 ERROR HANDLING

### Common Issues & Solutions

**Issue 1: Instagram Login Fails**
- **Cause:** Wrong credentials or account flagged
- **Solution:** Verify `.env` credentials, use 2FA, wait 24 hours if flagged
- **Retry:** Max 3 attempts with 5-minute delays

**Issue 2: Video Generation Fails**
- **Cause:** Missing fonts, PIL errors
- **Solution:** Install required fonts, check PIL version
- **Fallback:** Use backup pre-rendered video

**Issue 3: Context Overflow (Cheenu)**
- **Cause:** Too much conversation history
- **Solution:** Start fresh conversation, provide only this document
- **Prompt:** "Use AUTOMATION_GUIDE.md to create today's video"

**Issue 4: API Rate Limits**
- **Cause:** Too many requests to Instagram API
- **Solution:** Respect rate limits (10 posts/hour max)
- **Retry:** Exponential backoff (1min, 5min, 15min)

**Issue 5: Session Expired**
- **Cause:** Instagram session older than 90 days
- **Solution:** Delete `session.json`, script will re-authenticate
- **Prevention:** Refresh session every 30 days

---

## 📈 SUCCESS METRICS

### Track Daily:
- ✅ Video generated successfully
- ✅ Posted to Instagram
- ✅ Post URL logged
- ✅ No errors in execution

### Monitor Weekly:
- Views per video
- Likes, comments, saves
- Follower growth
- Engagement rate (saves ÷ views)

### Log Format:
```json
{
  "date": "2026-02-07",
  "content_type": "rasi",
  "content_title": "Taurus",
  "video_path": "./output/VedicDose_20260207_Taurus.mp4",
  "post_url": "https://instagram.com/p/ABC123/",
  "success": true,
  "error": null,
  "metrics": {
    "views_24h": 0,
    "likes_24h": 0,
    "saves_24h": 0
  }
}
```

---

## 🚀 QUICK START FOR CHEENU

### When You Receive This Prompt:

**1. Read this entire document first**
**2. Check if today's video is needed:**
   ```python
   import datetime
   today = datetime.datetime.now().strftime("%Y-%m-%d")
   # Check if video for today already exists in logs
   ```

**3. Execute automation:**
   ```bash
   cd /path/to/vedicdose
   python3 automation_master.py
   ```

**4. Verify success:**
   - Check logs/automation.log
   - Verify video in output/ folder
   - Confirm Instagram post live

**5. Report status:**
   - If success: "✅ VedicDose video posted: [URL]"
   - If failure: "❌ Error: [error message]"

---

## 📞 ESCALATION

**If automation fails 3 times:**
1. Log detailed error
2. Send alert to Laxy
3. Use backup pre-rendered video
4. Wait for manual intervention

**Contact:**
- **Laxy:** Primary owner
- **Cheenu:** cheenu.robot@gmail.com
- **GitHub:** https://github.com/laxy-17/cheenu-robot/tree/main/vedicdose

---

## 📚 RELATED DOCUMENTS

- `SECURITY.md` - API key protection
- `VIDEO_SPECS.md` - Design specifications
- `INSTAGRAM_STRATEGY.md` - Growth tactics
- `content_calendar.json` - 30-day rotation
- `.env.example` - Required environment variables

---

**Last Updated:** February 7, 2026  
**Version:** 1.0  
**Maintainer:** Laxy (ASTRAI Solutions LLC)
