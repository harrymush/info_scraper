# Info Scraper

A modern OSINT tool with a sleek GUI interface for searching usernames and email addresses across multiple platforms.

## Features

- **Username Search**: Check username availability across multiple platforms
- **Email Breach Check**: Verify if an email has been involved in data breaches
- **Detailed Profile Information**: Gather comprehensive data from each platform
- **Modern GUI**: Sleek dark theme interface with macOS-inspired design
- **Real-time Progress**: Visual feedback during searches
- **Save Results**: Export search results to text files

### Supported Platforms

- Twitter (name, bio, followers, following)
- GitHub (name, bio, latest repositories)
- Instagram (name, bio, followers)
- LinkedIn (name, headline, location)
- Facebook (name, bio)
- YouTube (name, subscribers, latest videos)
- Pinterest (name, bio, latest boards)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/harrymush/info_scraper.git
cd info_scraper
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the GUI application:
```bash
python osint_scout_gui.py
```

2. Enter a username or email address in the search field
3. Select the search type (Username or Email)
4. Click "Search" to begin the search
5. Results will be displayed in real-time
6. Click "Save Results" to export the findings to a text file

## Requirements

- Python 3.6+
- tkinter
- ttkthemes
- requests
- beautifulsoup4

## Project Structure

```
info_scraper/
├── osint_scout_gui.py      # Main GUI application
├── modules/
│   ├── usernames.py        # Username search functionality
│   └── email_breach.py     # Email breach checking
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- BeautifulSoup for web scraping capabilities
- ttkthemes for the modern GUI theme
- Have I Been Pwned API for email breach data
