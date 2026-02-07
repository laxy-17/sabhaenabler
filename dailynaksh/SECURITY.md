# VedicDose Security Guidelines

**CRITICAL:** This document outlines security requirements for the VedicDose automation system.

---

## 🔐 API KEY PROTECTION

### NEVER Commit These Files to Git:
- `.env` - Environment variables with secrets
- `.env.*` - Any environment file variants
- `session.json` - Instagram session data
- `*.key` - Any key files
- `credentials.json` - OAuth credentials
- `config.json` - If contains secrets

---

## 📝 REQUIRED: .gitignore File

**Ensure your `.gitignore` includes:**

```gitignore
# Environment variables
.env
.env.*
*.env

# API Keys
*.key
*_SECRET*
credentials.json

# Instagram Session
session.json
*.session

# Logs (may contain sensitive data)
logs/*.log
*.log

# Output files
output/*.mp4
output/*.jpg
output/*.png

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# OS
.DS_Store
Thumbs.db
.idea/
.vscode/
```

---

## 🔑 REQUIRED: .env File (NOT IN GIT)

**Create `.env` file with:**

```bash
# Instagram Credentials
INSTAGRAM_USERNAME=vedic.dose
INSTAGRAM_PASSWORD=your_secure_password_here

# Instagram Session (auto-generated)
INSTAGRAM_SESSION_FILE=./session.json

# Optional: AI APIs
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Notifications
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
```

**NEVER commit this file to Git!**

---

## ✅ REQUIRED: .env.example File (IN GIT)

**Create `.env.example` as template:**

```bash
# Instagram Credentials
INSTAGRAM_USERNAME=your_username_here
INSTAGRAM_PASSWORD=your_password_here

# Instagram Session
INSTAGRAM_SESSION_FILE=./session.json

# Optional: AI APIs
GEMINI_API_KEY=your_api_key_here

# Optional: Notifications
SLACK_WEBHOOK_URL=your_webhook_url_here
```

**This file shows structure but has no real values.**

---

## 🛡️ SECURITY BEST PRACTICES

### 1. Environment Variable Loading

**Always use python-dotenv:**

```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access variables
username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')

# NEVER hardcode:
# username = "vedic.dose"  ❌ WRONG!
# password = "my_password"  ❌ WRONG!
```

### 2. Verify .gitignore Before Commits

**Before every git commit:**

```bash
# Check what will be committed
git status

# Verify no sensitive files
git ls-files | grep -E '\.env|session\.json|\.key'

# Should return nothing!
```

### 3. Session Management

**Instagram session is cached to avoid repeated logins:**

- Session saved in `session.json`
- Automatically reused on subsequent runs
- Expires after ~90 days
- Delete file to force re-authentication

```python
from instagrapi import Client

cl = Client()
session_file = "session.json"

# Try to load existing session
if os.path.exists(session_file):
    cl.load_settings(session_file)
    cl.login(username, password)
else:
    # First login
    cl.login(username, password)
    cl.dump_settings(session_file)
```

### 4. Error Messages

**NEVER expose secrets in logs:**

```python
# ❌ WRONG - exposes password
logger.error(f"Login failed with password: {password}")

# ✅ CORRECT - generic message
logger.error("Login failed. Check credentials in .env file")
```

### 5. Git History Check

**If you accidentally committed secrets:**

```bash
# Search Git history for API keys
git log -p | grep -i "api_key\|password\|secret"

# If found, use BFG Repo-Cleaner or git filter-branch
# Better: Create new keys and revoke old ones
```

---

## 🚨 IF API KEYS ARE EXPOSED

**Immediate actions:**

1. **Revoke compromised keys immediately**
   - Instagram: Change password, enable 2FA
   - Google/Gemini: Regenerate API key in console
   - Slack: Regenerate webhook URL

2. **Remove from Git history**
   ```bash
   # Install BFG Repo-Cleaner
   # https://rtyley.github.io/bfg-repo-cleaner/
   
   java -jar bfg.jar --delete-files .env
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push --force
   ```

3. **Update .gitignore**
   - Ensure .env is listed
   - Commit updated .gitignore
   - Verify with `git status`

4. **Generate new keys**
   - Update `.env` with new credentials
   - Test automation with new keys
   - Document incident in security log

---

## 🔍 PRE-COMMIT CHECKLIST

Before running `git commit`:

- [ ] `.env` file is NOT staged (`git status`)
- [ ] `session.json` is NOT staged
- [ ] No `*.key` files staged
- [ ] `.gitignore` is up to date
- [ ] No hardcoded passwords in code
- [ ] All secrets loaded from environment variables
- [ ] Error messages don't expose secrets
- [ ] Logs don't contain sensitive data

**Use this command to verify:**
```bash
git diff --cached | grep -E 'password|api_key|secret|token' -i
```

If anything found → **DO NOT COMMIT!**

---

## 📦 DEPENDENCY SECURITY

**Keep packages updated:**

```bash
# Check for vulnerable packages
pip list --outdated

# Update packages
pip install --upgrade --break-system-packages instagrapi pillow moviepy

# Review security advisories
pip-audit
```

---

## 🔐 TWO-FACTOR AUTHENTICATION

**Instagram 2FA Setup:**

1. Enable 2FA in Instagram settings
2. Use authenticator app (Google Authenticator)
3. Save backup codes securely
4. Update `.env` with 2FA settings if needed

**For automation:**
- Use session persistence (`session.json`)
- Reuses authenticated session
- Avoids repeated 2FA challenges

---

## 📝 SECURITY AUDIT CHECKLIST

**Monthly review:**

- [ ] Rotate Instagram password
- [ ] Check Git history for exposed secrets
- [ ] Review `.gitignore` completeness
- [ ] Update dependencies for security patches
- [ ] Verify session file permissions (600)
- [ ] Check logs for suspicious activity
- [ ] Test backup & restore procedures

---

## 🆘 INCIDENT RESPONSE

**If security breach suspected:**

1. **Immediate:**
   - Revoke all API keys
   - Change all passwords
   - Delete `session.json`
   - Review recent Instagram activity

2. **Investigation:**
   - Check Git history for commits
   - Review access logs
   - Identify exposure timeline
   - Document findings

3. **Recovery:**
   - Generate new credentials
   - Update `.env` file
   - Re-test automation
   - Monitor for 48 hours

4. **Prevention:**
   - Update `.gitignore`
   - Add pre-commit hooks
   - Document lessons learned
   - Train team on security

---

## 📞 SECURITY CONTACTS

**Report security issues:**
- Email: cheenu.robot@gmail.com
- GitHub: Create private security advisory
- Urgent: Contact Laxy directly

---

## 📚 ADDITIONAL RESOURCES

- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Instagram API Guidelines](https://developers.facebook.com/docs/instagram-api)

---

**Last Updated:** February 7, 2026  
**Version:** 1.0  
**Security Level:** CRITICAL
