#!/usr/bin/env python3
"""
VedicDose Automation Master Script
Creates and posts daily Instagram Reel automatically

Usage:
    python3 automation_master.py
    
Environment variables required in .env:
    INSTAGRAM_USERNAME
    INSTAGRAM_PASSWORD
"""

import os
import sys
import json
import datetime
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def get_today_content():
    """Determine today's content based on day of month"""
    day = datetime.datetime.now().day % 30
    if day == 0:
        day = 30
    
    # Load content calendar
    calendar_path = Path("content_calendar.json")
    if not calendar_path.exists():
        logger.error("content_calendar.json not found!")
        return None
    
    with open(calendar_path, 'r', encoding='utf-8') as f:
        calendar = json.load(f)
    
    content = calendar.get(str(day))
    if not content:
        logger.error(f"No content defined for day {day}")
        return None
    
    logger.info(f"Today's content: {content['type']} - {content['title_english']}")
    return content


def generate_video(content):
    """Generate video using video_generator.py"""
    from scripts.video_generator import create_indianized_video
    
    logger.info("Generating video...")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"VedicDose_{timestamp}_{content['title_english'].replace(' ', '_')}.mp4"
    output_path = output_dir / filename
    
    try:
        video_path = create_indianized_video(content, str(output_path))
        logger.info(f"✅ Video created: {video_path}")
        return video_path
    except Exception as e:
        logger.error(f"❌ Video generation failed: {str(e)}")
        raise


def generate_caption(content):
    """Generate Instagram caption with hashtags"""
    from scripts.caption_generator import create_caption
    
    logger.info("Generating caption...")
    caption = create_caption(content)
    
    # Save caption to file
    output_dir = Path("output")
    caption_file = output_dir / "latest_caption.txt"
    
    with open(caption_file, 'w', encoding='utf-8') as f:
        f.write(caption)
    
    logger.info(f"✅ Caption generated ({len(caption)} chars)")
    return caption


def post_to_instagram(video_path, caption):
    """Post video to Instagram using instagrapi"""
    from scripts.instagram_poster import upload_reel
    
    logger.info("Posting to Instagram...")
    
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    
    if not username or not password:
        raise ValueError("Instagram credentials not found in .env file")
    
    try:
        result = upload_reel(
            username=username,
            password=password,
            video_path=video_path,
            caption=caption
        )
        
        if result['success']:
            logger.info(f"✅ Posted successfully: {result['url']}")
        else:
            logger.error(f"❌ Posting failed: {result['error']}")
        
        return result
    
    except Exception as e:
        logger.error(f"❌ Instagram posting error: {str(e)}")
        return {'success': False, 'error': str(e)}


def log_execution(content, video_path, post_result):
    """Log execution details to posting_log.json"""
    log_file = Path("logs/posting_log.json")
    
    # Load existing logs
    if log_file.exists():
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    # Add today's log entry
    log_entry = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.datetime.now().isoformat(),
        "content_type": content['type'],
        "content_title": content['title_english'],
        "video_path": str(video_path),
        "post_url": post_result.get('url'),
        "success": post_result.get('success', False),
        "error": post_result.get('error')
    }
    
    logs.append(log_entry)
    
    # Save updated logs
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    logger.info("Execution logged to posting_log.json")


def main():
    """Main execution function"""
    logger.info("=" * 60)
    logger.info("🚀 VedicDose Automation Started")
    logger.info("=" * 60)
    
    try:
        # Step 1: Get today's content
        logger.info("📅 Step 1: Determining today's content...")
        content = get_today_content()
        if not content:
            logger.error("❌ Could not determine today's content")
            return 1
        
        # Step 2: Generate video
        logger.info("🎬 Step 2: Generating video...")
        video_path = generate_video(content)
        
        # Step 3: Generate caption
        logger.info("✍️  Step 3: Generating caption...")
        caption = generate_caption(content)
        
        # Step 4: Post to Instagram
        logger.info("📱 Step 4: Posting to Instagram...")
        post_result = post_to_instagram(video_path, caption)
        
        # Step 5: Log execution
        logger.info("📝 Step 5: Logging execution...")
        log_execution(content, video_path, post_result)
        
        # Summary
        logger.info("=" * 60)
        if post_result['success']:
            logger.info("✅ AUTOMATION SUCCESSFUL!")
            logger.info(f"📍 Post URL: {post_result['url']}")
            print(f"\n✅ SUCCESS! Video posted: {post_result['url']}\n")
            return 0
        else:
            logger.error("❌ AUTOMATION FAILED")
            logger.error(f"Error: {post_result['error']}")
            print(f"\n❌ FAILED: {post_result['error']}\n")
            return 1
    
    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR: {str(e)}", exc_info=True)
        print(f"\n❌ CRITICAL ERROR: {str(e)}\n")
        return 1
    
    finally:
        logger.info("=" * 60)
        logger.info("🏁 VedicDose Automation Completed")
        logger.info("=" * 60)


if __name__ == "__main__":
    sys.exit(main())
