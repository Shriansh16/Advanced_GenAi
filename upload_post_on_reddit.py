import praw
import groq
import schedule
import time
import logging
from datetime import datetime, timedelta
import os
from groq import Groq
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_reddit_instance():
    """Create and return a Reddit instance using PRAW."""
    try:
        reddit = praw.Reddit(
            client_id="",
            client_secret="",
            user_agent=")",
            username="",
            password=""
        )
        return reddit
    except Exception as e:
        logger.error(f"Error creating Reddit instance: {e}")
        raise

def submit_post(subreddit_name, title, content, post_type='text'):
    """Submit a post to a specified subreddit."""
    reddit = create_reddit_instance()
    try:
        subreddit = reddit.subreddit(subreddit_name)
        if not subreddit.user_is_subscriber:
            logger.warning(f"Warning: You are not subscribed to r/{subreddit_name}")
        
        if post_type == 'text':
            submission = subreddit.submit(title=title, selftext=content)
        elif post_type == 'link':
            submission = subreddit.submit(title=title, url=content)
        else:
            raise ValueError("Invalid post_type. Use 'text' or 'link'")
        
        logger.info(f"Post successfully submitted to r/{subreddit_name}")
        return submission.url
    except Exception as e:
        logger.error(f"Error submitting post: {e}")
        return None

def generate_ai_content(subject):
    """Generate AI content using Groq."""
    try:
        load_dotenv()
        groqkey = os.getenv('GROQ_API_KEY')
        client = Groq(api_key=groqkey)
        
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Reddit post generator. Create engaging and interesting subreddit posts."
                },
                {
                    "role": "user",
                    "content": f"Create an engaging and interesting subreddit post about {subject}."
                }
            ],
            temperature=0.3,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating AI content: {e}")
        return None

def create_scheduled_post():
    """Create and submit a scheduled post."""
    try:
        subject = "Artificial Intelligence"  # You can modify this or make it dynamic
        content = generate_ai_content(subject)
        if content:
            post_url = submit_post(
                subreddit_name="test",
                title=subject,
                content=content,
                post_type='text'
            )
            logger.info(f"Scheduled post created successfully: {post_url}")
        else:
            logger.error("Failed to generate content")
    except Exception as e:
        logger.error(f"Error in scheduled post creation: {e}")

def schedule_post_in_five_minutes():
    """Schedule a post to be created in 5 minutes from now."""
    # Get current time
    current_time = datetime.now()
    # Calculate posting time (5 minutes from now)
    posting_time = current_time + timedelta(minutes=5)
    # Format time for scheduler
    schedule_time = posting_time.strftime("%H:%M")
    
    logger.info(f"Scheduling post for {schedule_time}")
    schedule.every().day.at(schedule_time).do(create_scheduled_post)
    
    # Run until the post is made
    while True:
        schedule.run_pending()
        time.sleep(1)
        # Check if we've passed the scheduled time
        if datetime.now() > posting_time + timedelta(minutes=1):
            break

if __name__ == "__main__":
    logger.info("Starting scheduler for post in 5 minutes...")
    schedule_post_in_five_minutes()
    logger.info("Post has been scheduled and executed. Program ending.")
