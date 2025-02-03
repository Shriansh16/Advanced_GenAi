import praw
import sys
from datetime import datetime

def create_reddit_instance():
    """
    Create and return a Reddit instance using PRAW.
    Make sure to replace the placeholder values with your actual credentials.
    """
    try:
        reddit = praw.Reddit(
            client_id="dR3XNR8_eMd2b2yw9iMhpg",
            client_secret="VfW-2yydC88LfK2sUKA_gK3zzm-SAg",
            user_agent="script:post_creator:v1.0 (by /u/brucewayne)",
            username="MuchFootball4622",
            password="shriansh99"
        )
        return reddit
    except Exception as e:
        print(f"Error creating Reddit instance: {e}")
        sys.exit(1)

def submit_post(subreddit_name, title, content, post_type='text'):
    """
    Submit a post to a specified subreddit.
    
    Parameters:
    - subreddit_name: Name of the subreddit to post to
    - title: Title of the post
    - content: Content of the post (text body or URL)
    - post_type: 'text' or 'link' (default: 'text')
    
    Returns:
    - URL of the created post if successful
    """
    reddit = create_reddit_instance()
    
    try:
        # Get the subreddit instance
        subreddit = reddit.subreddit(subreddit_name)
        
        # Check if we have permission to post
        if not subreddit.user_is_subscriber:
            print(f"Warning: You are not subscribed to r/{subreddit_name}")
        
        # Submit the post based on type
        if post_type == 'text':
            submission = subreddit.submit(title=title, selftext=content)
        elif post_type == 'link':
            submission = subreddit.submit(title=title, url=content)
        else:
            raise ValueError("Invalid post_type. Use 'text' or 'link'")
        
        print(f"Post successfully submitted to r/{subreddit_name}")
        return submission.url
        
    except praw.exceptions.RedditAPIException as e:
        print(f"Reddit API Error: {e}")
    except Exception as e:
        print(f"Error submitting post: {e}")
    
    return None

# Example usage
if __name__ == "__main__":
    # Example text post
    text_post_url = submit_post(
        subreddit_name="test",
        title="Test Post from Python Script",
        content="This is a test post created using PRAW!",
        post_type='text'
    )