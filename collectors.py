import praw
import feedparser
import requests
from datetime import datetime
from config import (
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT,
    REDDIT_SUBREDDITS, REDDIT_SEARCH_KEYWORDS, REDDIT_POSTS_PER_SUBREDDIT,
    BLUESKY_USERNAME, BLUESKY_PASSWORD
)

class RedditCollector:
    """Collect posts from Reddit."""

    def __init__(self):
        self.reddit = None
        if REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET:
            self.reddit = praw.Reddit(
                client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent=REDDIT_USER_AGENT
            )

    def collect_from_subreddits(self, subreddits=None, limit=None):
        """Collect posts from subreddits."""
        if not self.reddit:
            print("Reddit API not configured. Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET.")
            return []

        subreddits = subreddits or REDDIT_SUBREDDITS
        limit = limit or REDDIT_POSTS_PER_SUBREDDIT
        posts = []

        for subreddit_name in subreddits:
            try:
                print(f"Collecting from r/{subreddit_name}...")
                subreddit = self.reddit.subreddit(subreddit_name)

                for post in subreddit.new(limit=limit):
                    posts.append({
                        "id": f"reddit_{post.id}",
                        "platform": "reddit",
                        "author": post.author.name if post.author else "[deleted]",
                        "title": post.title,
                        "content": f"{post.title}\n\n{post.selftext}",
                        "url": post.url,
                        "created_at": datetime.fromtimestamp(post.created_utc),
                        "source_metadata": {
                            "subreddit": subreddit_name,
                            "score": post.score,
                            "num_comments": post.num_comments,
                            "reddit_id": post.id
                        }
                    })

                print(f"  Collected {len([p for p in posts if p['platform'] == 'reddit' and subreddit_name in str(p.get('source_metadata', {}))])} posts from r/{subreddit_name}")

            except Exception as e:
                print(f"Error collecting from r/{subreddit_name}: {e}")

        return posts

    def search_posts(self, keywords=None, limit=10):
        """Search Reddit for specific keywords."""
        if not self.reddit:
            print("Reddit API not configured.")
            return []

        keywords = keywords or REDDIT_SEARCH_KEYWORDS
        posts = []

        for keyword in keywords:
            try:
                print(f"Searching Reddit for '{keyword}'...")
                for post in self.reddit.subreddit("all").search(keyword, time_filter="week", limit=limit):
                    posts.append({
                        "id": f"reddit_{post.id}",
                        "platform": "reddit",
                        "author": post.author.name if post.author else "[deleted]",
                        "title": post.title,
                        "content": f"{post.title}\n\n{post.selftext}",
                        "url": post.url,
                        "created_at": datetime.fromtimestamp(post.created_utc),
                        "source_metadata": {
                            "subreddit": post.subreddit.display_name,
                            "search_keyword": keyword,
                            "score": post.score
                        }
                    })
            except Exception as e:
                print(f"Error searching for '{keyword}': {e}")

        return posts

class RSSCollector:
    """Collect threat reports from RSS feeds."""

    def __init__(self):
        self.feeds = [
            "https://www.bleepingcomputer.com/feed/",
            "https://feeds.securityonline.info/rss",
            "https://feeds.oreilly.com/topics/security",
        ]

    def collect_from_feeds(self):
        """Collect posts from RSS feeds."""
        posts = []

        for feed_url in self.feeds:
            try:
                print(f"Collecting from {feed_url}...")
                feed = feedparser.parse(feed_url)

                for entry in feed.entries[:50]:
                    posts.append({
                        "id": f"rss_{feed_url.split('/')[-2]}_{entry.get('id', entry.get('link', ''))}",
                        "platform": "rss_feed",
                        "author": entry.get('author', 'Unknown'),
                        "title": entry.get('title', ''),
                        "content": entry.get('summary', ''),
                        "url": entry.get('link', ''),
                        "created_at": datetime(*entry.published_parsed[:6]) if 'published_parsed' in entry else datetime.now(),
                        "source_metadata": {
                            "feed_url": feed_url,
                            "feed_title": feed.feed.get('title', 'Unknown')
                        }
                    })

                print(f"  Collected {len([p for p in posts if p['platform'] == 'rss_feed'])} posts")

            except Exception as e:
                print(f"Error collecting from {feed_url}: {e}")

        return posts

class BlueskyCollector:
    """Collect posts from Bluesky (via public API)."""

    def __init__(self):
        self.base_url = "https://bsky.social/xrpc"

    def search_posts(self, keywords=None, limit=100):
        """Search Bluesky for keywords (public API)."""
        keywords = keywords or ["recruitment scam", "deepfake interview", "fake recruiter"]
        posts = []

        try:
            # Note: This is a simplified implementation.
            # Full Bluesky integration would require proper AT Protocol authentication.
            print("Bluesky collection requires AT Protocol authentication (not yet implemented)")
            return posts

        except Exception as e:
            print(f"Error collecting from Bluesky: {e}")
            return posts

def collect_all_sources(reddit_enabled=True, rss_enabled=True, bluesky_enabled=False):
    """Orchestrate collection from all sources."""
    all_posts = []

    if reddit_enabled:
        reddit_collector = RedditCollector()
        print("\n=== Collecting from Reddit ===")
        all_posts.extend(reddit_collector.collect_from_subreddits())
        all_posts.extend(reddit_collector.search_posts())

    if rss_enabled:
        rss_collector = RSSCollector()
        print("\n=== Collecting from RSS Feeds ===")
        all_posts.extend(rss_collector.collect_from_feeds())

    if bluesky_enabled:
        bluesky_collector = BlueskyCollector()
        print("\n=== Collecting from Bluesky ===")
        all_posts.extend(bluesky_collector.search_posts())

    print(f"\n=== Total posts collected: {len(all_posts)} ===")
    return all_posts
