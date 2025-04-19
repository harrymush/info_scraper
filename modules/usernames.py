import requests
from bs4 import BeautifulSoup
import re
import time

PLATFORMS = {
    "GitHub": {
        "url": "https://github.com/{}",
        "check": lambda r: r.status_code == 200 and "This is not the web page you are looking for" not in r.text
    },
    "Twitter": {
        "url": "https://twitter.com/{}",
        "check": lambda r: r.status_code == 200 and "This account doesn't exist" not in r.text
    },
    "Reddit": {
        "url": "https://www.reddit.com/user/{}",
        "check": lambda r: r.status_code == 200 and "Sorry, nobody on Reddit goes by that name" not in r.text
    },
    "Instagram": {
        "url": "https://www.instagram.com/{}",
        "check": lambda r: r.status_code == 200 and "Sorry, this page isn't available" not in r.text
    },
    "TikTok": {
        "url": "https://www.tiktok.com/@{}",
        "check": lambda r: r.status_code == 200 and "Couldn't find this account" not in r.text
    },
    "Facebook": {
        "url": "https://www.facebook.com/{}",
        "check": lambda r: r.status_code == 200 and "This page isn't available" not in r.text
    },
    "LinkedIn": {
        "url": "https://www.linkedin.com/in/{}",
        "check": lambda r: r.status_code == 200 and "This profile is not available" not in r.text
    },
    "Pinterest": {
        "url": "https://www.pinterest.com/{}",
        "check": lambda r: r.status_code == 200 and "Sorry, we couldn't find that page" not in r.text
    },
    "YouTube": {
        "url": "https://www.youtube.com/@{}",
        "check": lambda r: r.status_code == 200 and "This channel doesn't exist" not in r.text
    }
}

def get_profile_info(url, platform):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if platform == "GitHub":
                name = soup.find('span', {'itemprop': 'name'})
                bio = soup.find('div', {'class': 'p-note'})
                return {
                    'name': name.text.strip() if name else None,
                    'bio': bio.text.strip() if bio else None
                }
            elif platform == "Twitter":
                name = soup.find('div', {'data-testid': 'UserName'})
                bio = soup.find('div', {'data-testid': 'UserDescription'})
                return {
                    'name': name.text.strip() if name else None,
                    'bio': bio.text.strip() if bio else None
                }
            # Add more platform-specific scraping here
    except Exception as e:
        print(f"Error scraping {platform}: {str(e)}")
    return None

def check_username(username):
    results = {}
    
    # Twitter
    try:
        response = requests.get(f"https://twitter.com/{username}", timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('div', {'data-testid': 'UserName'})
            bio = soup.find('div', {'data-testid': 'UserDescription'})
            followers = soup.find('a', href=f'/{username}/followers')
            following = soup.find('a', href=f'/{username}/following')
            
            results['Twitter'] = {
                'exists': True,
                'url': f"https://twitter.com/{username}",
                'profile_info': {
                    'name': name.text.strip() if name else None,
                    'bio': bio.text.strip() if bio else None,
                    'followers': followers.text.strip() if followers else None,
                    'following': following.text.strip() if following else None
                }
            }
    except:
        pass

    # GitHub
    try:
        response = requests.get(f"https://github.com/{username}", timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('span', {'itemprop': 'name'})
            bio = soup.find('div', {'class': 'p-note'})
            repos = soup.find_all('a', {'itemprop': 'name codeRepository'})
            latest_repos = [repo.text.strip() for repo in repos[:3]]  # Get 3 latest repos
            
            results['GitHub'] = {
                'exists': True,
                'url': f"https://github.com/{username}",
                'profile_info': {
                    'name': name.text.strip() if name else None,
                    'bio': bio.text.strip() if bio else None,
                    'latest_repos': latest_repos if latest_repos else None
                }
            }
    except:
        pass

    # Instagram
    try:
        response = requests.get(f"https://www.instagram.com/{username}/", timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('h1')
            bio = soup.find('div', {'class': '-vDIg'})
            followers = soup.find('meta', {'property': 'og:description'})
            
            results['Instagram'] = {
                'exists': True,
                'url': f"https://www.instagram.com/{username}/",
                'profile_info': {
                    'name': name.text.strip() if name else None,
                    'bio': bio.text.strip() if bio else None,
                    'followers': followers.get('content') if followers else None
                }
            }
    except:
        pass

    # LinkedIn
    try:
        response = requests.get(f"https://www.linkedin.com/in/{username}/", timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('h1', {'class': 'text-heading-xlarge'})
            headline = soup.find('div', {'class': 'text-body-medium'})
            location = soup.find('span', {'class': 'text-body-small'})
            
            results['LinkedIn'] = {
                'exists': True,
                'url': f"https://www.linkedin.com/in/{username}/",
                'profile_info': {
                    'name': name.text.strip() if name else None,
                    'headline': headline.text.strip() if headline else None,
                    'location': location.text.strip() if location else None
                }
            }
    except:
        pass

    # Facebook
    try:
        response = requests.get(f"https://www.facebook.com/{username}", timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('title')
            bio = soup.find('div', {'class': '_4-u2 _4-u8'})
            
            results['Facebook'] = {
                'exists': True,
                'url': f"https://www.facebook.com/{username}",
                'profile_info': {
                    'name': name.text.strip() if name else None,
                    'bio': bio.text.strip() if bio else None
                }
            }
    except:
        pass

    # YouTube
    try:
        response = requests.get(f"https://www.youtube.com/@{username}", timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('yt-formatted-string', {'id': 'text'})
            subscribers = soup.find('yt-formatted-string', {'id': 'subscriber-count'})
            videos = soup.find_all('ytd-grid-video-renderer')[:3]  # Get 3 latest videos
            latest_videos = [video.find('a', {'id': 'video-title'}).text.strip() for video in videos if video.find('a', {'id': 'video-title'})]
            
            results['YouTube'] = {
                'exists': True,
                'url': f"https://www.youtube.com/@{username}",
                'profile_info': {
                    'name': name.text.strip() if name else None,
                    'subscribers': subscribers.text.strip() if subscribers else None,
                    'latest_videos': latest_videos if latest_videos else None
                }
            }
    except:
        pass

    # Pinterest
    try:
        response = requests.get(f"https://www.pinterest.com/{username}/", timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find('h1')
            bio = soup.find('div', {'class': 'ProfileHeader-bio'})
            boards = soup.find_all('div', {'class': 'Board'})[:3]  # Get 3 latest boards
            latest_boards = [board.find('h2').text.strip() for board in boards if board.find('h2')]
            
            results['Pinterest'] = {
                'exists': True,
                'url': f"https://www.pinterest.com/{username}/",
                'profile_info': {
                    'name': name.text.strip() if name else None,
                    'bio': bio.text.strip() if bio else None,
                    'latest_boards': latest_boards if latest_boards else None
                }
            }
    except:
        pass

    return results
