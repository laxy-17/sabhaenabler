# VedicDose Instagram Automation

**Automated daily Instagram Reel creation and posting system for @vedic.dose**

---

## 🌟 Overview

VedicDose is an automated content creation system that generates and posts daily Vedic astrology Reels to Instagram. The system creates 30-second videos featuring:

- **12 Rasi (Zodiac Signs)** - Personality traits and characteristics
- **27 Nakshatras (Birth Stars)** - Deep dives into lunar mansions
- **Daily Transits** - Cosmic energy guidance
- **Vedic Tips** - Quick actionable wisdom

**Style:** Indianized Vedic aesthetic with Devanagari text, mandala patterns, and traditional design elements.

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/laxy-17/cheenu-robot.git
cd cheenu-robot/vedicdose
```

### 2. Install Dependencies
```bash
pip install --break-system-packages -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required in .env:**
- `INSTAGRAM_USERNAME` - Your Instagram username
- `INSTAGRAM_PASSWORD` - Your Instagram password

### 4. Test Run
```bash
python3 automation_master.py
```

This will:
1. Generate today's video (based on day of month)
2. Create caption with hashtags
3. Post to Instagram @vedic.dose
4. Log execution results

---

## 📁 Project Structure

```
vedicdose/
├── automation_master.py     # Main execution script
├── AUTOMATION_GUIDE.md      # Detailed automation guide
├── SECURITY.md              # Security best practices
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git exclusions
├── content_calendar.json   # 30-day content rotation
├── scripts/
│   ├── video_generator.py   # Video creation logic
│   ├── instagram_poster.py  # Instagram API posting
│   ├── caption_generator.py # Dynamic captions
│   └── content_selector.py  # Daily content logic
├── templates/
│   ├── rasi_template.py     # Zodiac video templates
│   ├── nakshatra_template.py
│   ├── transit_template.py
│   └── tip_template.py
├── data/
│   ├── rasi_data.json
│   ├── nakshatra_data.json
│   └── tips_data.json
├── output/                  # Generated videos (gitignored)
└── logs/                    # Execution logs (gitignored)
```

---

## 🎨 Video Specifications

- **Resolution:** 1080x1920 (Instagram Reel format)
- **Duration:** 30 seconds
- **FPS:** 30
- **Colors:** Navy (#0a0a1f) + Gold (#d4af37) + Saffron (#ff9933)
- **Audio:** 432 Hz ambient tone (sacred Vedic frequency)

**Design Elements:**
- Devanagari/Sanskrit text
- Mandala background patterns
- Rangoli-style decorative elements
- Traditional Indian borders
- Smooth fade-in animations

---

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Instagram Credentials (REQUIRED)
INSTAGRAM_USERNAME=vedic.dose
INSTAGRAM_PASSWORD=your_password

# Session Management
INSTAGRAM_SESSION_FILE=./session.json

# Optional: AI APIs
GEMINI_API_KEY=your_key_here

# Optional: Notifications
SLACK_WEBHOOK_URL=your_webhook_url
```

**Security:** Never commit `.env` to Git! Use `.env.example` as template.

---

## 📅 Content Calendar

Content rotates on 30-day cycle based on day of month:

- **Days 1-3:** Fire signs (Aries, Leo, Sagittarius)
- **Days 4-6:** Earth signs (Taurus, Virgo, Capricorn)
- **Days 7-9:** Air signs (Gemini, Libra, Aquarius)
- **Days 10-12:** Water signs (Cancer, Scorpio, Pisces)
- **Days 13-27:** Nakshatras (Ashwini through Revati)
- **Days 28-30:** Quick tips & remedies

Edit `content_calendar.json` to customize content.

---

## 🤖 Automation Setup

### Option 1: Make.com (Recommended)

1. Create Make.com account (free tier)
2. New Scenario → Schedule trigger (7:00 AM IST daily)
3. Add Webhook → Call your server
4. Webhook executes: `python3 automation_master.py`

### Option 2: Cron Job

```bash
# Add to crontab (crontab -e)
# Runs daily at 7:00 AM IST (1:30 AM UTC)
30 1 * * * cd /path/to/vedicdose && python3 automation_master.py >> logs/cron.log 2>&1
```

### Option 3: Manual

```bash
# Run anytime
python3 automation_master.py
```

---

## 📊 Logging & Monitoring

### Execution Logs
```bash
# View automation logs
tail -f logs/automation.log

# View posting history
cat logs/posting_log.json
```

### Log Format
```json
{
  "date": "2026-02-07",
  "content_type": "rasi",
  "content_title": "Taurus",
  "video_path": "./output/VedicDose_20260207_Taurus.mp4",
  "post_url": "https://instagram.com/p/ABC123/",
  "success": true,
  "error": null
}
```

---

## 🔒 Security

**Critical Files (NEVER commit to Git):**
- `.env` - Contains passwords and API keys
- `session.json` - Instagram session data
- `logs/*.log` - May contain sensitive info
- `output/*.mp4` - Generated videos (optional)

**Verify security:**
```bash
# Check what will be committed
git status

# Search for sensitive patterns
git diff --cached | grep -E 'password|api_key|secret' -i
```

See `SECURITY.md` for complete security guidelines.

---

## 📈 Success Metrics

### Track Daily:
- Video generated successfully
- Posted to Instagram without errors
- Post URL logged

### Monitor Weekly:
- View count per video
- Engagement rate (likes + comments + saves ÷ views)
- Follower growth
- Save rate (most important metric)

---

## 🐛 Troubleshooting

### Issue: Instagram Login Fails
```bash
# Delete session and retry
rm session.json
python3 automation_master.py
```

### Issue: Video Generation Fails
```bash
# Check logs
cat logs/automation.log

# Verify dependencies
pip list | grep -E "moviepy|pillow|numpy"
```

### Issue: "Context Overflow" (for Cheenu)
**Solution:** Start fresh conversation with minimal prompt:
```
Use AUTOMATION_GUIDE.md to create and post today's VedicDose video.
Execute: python3 automation_master.py
```

### Issue: Module Not Found
```bash
# Reinstall requirements
pip install --break-system-packages -r requirements.txt
```

---

## 📞 Support

- **Repository:** https://github.com/laxy-17/cheenu-robot/tree/main/vedicdose
- **Issues:** Create GitHub issue
- **Email:** cheenu.robot@gmail.com
- **Instagram:** @vedic.dose

---

## 📚 Documentation

- **AUTOMATION_GUIDE.md** - Complete automation workflow
- **SECURITY.md** - API key protection guidelines
- **VIDEO_SPECS.md** - Design specifications (TODO)
- **INSTAGRAM_STRATEGY.md** - Growth tactics (TODO)

---

## 🎯 Related Projects

### ASTRAI Platform
- **Domain:** astrai.com
- **Description:** Full Vedic astrology web application
- **Tech:** React, FastAPI, Supabase, Swiss Ephemeris
- **Launch:** January 11, 2026

VedicDose serves as content marketing for ASTRAI, building Instagram audience before app launch.

---

## 🔄 Version History

- **v1.0** (Feb 7, 2026) - Initial automation system
  - Basic video generation
  - Instagram posting
  - 30-day content calendar
  - Indianized design aesthetic

---

## 🙏 Credits

**Created by:** Laxy (Lakshmanan)  
**Company:** ASTRAI Solutions LLC  
**Numerology:** Number 5 (Mercury - Communication)  
**Brand Colors:** Navy (#0a0a1f) + Gold (#d4af37)

---

## 📜 License

Proprietary - ASTRAI Solutions LLC  
All rights reserved.

---

**Last Updated:** February 7, 2026  
**Status:** Production Ready  
**Instagram:** [@vedic.dose](https://instagram.com/vedic.dose)
