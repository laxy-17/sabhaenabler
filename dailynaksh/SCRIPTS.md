git init
touch README.md MEMORY.md CONFIG.md BRAND.md AI_MODELS.md CONTENT_CALENDAR.md SCRIPTS_LIBRARY.md DESIGN_SPECS.md MUSIC_LIBRARY.md AUTOMATION_WORKFLOW.md ASTROLOGY_DATA.md INSTAGRAM_STRATEGY.md LAUNCH_CHECKLIST.md
echo " .env *.key *_SECRET* node_modules/ __pycache__/ .DS_Store " > .gitignore
git remote add origin https://github.com/laxy-17/sabhaenabler.git
git add .
git commit -m "Initial commit: DailyNaksh project memory and configuration files"
git push -u origin main
