import tkinter as tk
from tkinter import ttk, scrolledtext
from ttkthemes import ThemedTk
import os
from datetime import datetime
from modules import usernames, email_breach
import threading
import queue
import time

class OSINTScoutGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Info Scraper")
        self.root.geometry("900x700")
        
        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use('arc')
        
        # Configure colors
        self.bg_color = '#2d2d2d'
        self.fg_color = '#ffffff'
        self.accent_color = '#808080'  # Made even lighter gray
        self.hover_color = '#909090'   # Lighter hover color
        self.secondary_color = '#3d3d3d'
        
        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', 
                           background=self.bg_color, 
                           foreground=self.fg_color, 
                           font=('Playfair Display', 10))
        self.style.configure('TButton', 
                           background=self.accent_color,
                           foreground=self.fg_color,
                           font=('Playfair Display', 10, 'bold'),
                           padding=10)
        self.style.configure('Accent.TButton',
                           background=self.accent_color,
                           foreground=self.fg_color,
                           font=('Playfair Display', 10, 'bold'),
                           padding=10)
        self.style.configure('TRadiobutton', 
                           background=self.bg_color,
                           foreground=self.fg_color,
                           font=('Playfair Display', 10))
        self.style.configure('TEntry', 
                           fieldbackground=self.secondary_color,
                           foreground=self.fg_color,
                           insertcolor=self.fg_color,
                           font=('Playfair Display', 10))
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        self.create_title()
        
        # Create search type selection
        self.search_type = tk.StringVar(value="username")
        self.create_search_type_selector()
        
        # Create input field
        self.create_input_field()
        
        # Create platform selection
        self.create_platform_selector()
        
        # Create search button
        self.create_search_button()
        
        # Create progress bar
        self.create_progress_bar()
        
        # Create results area
        self.create_results_area()
        
        # Create save button
        self.create_save_button()
        
        # Queue for thread communication
        self.queue = queue.Queue()
        
        # Start checking for updates
        self.root.after(100, self.check_queue)
    
    def create_title(self):
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="Info Scraper",
            font=('Playfair Display', 24, 'bold'),
            foreground=self.fg_color
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Search across multiple platforms",
            font=('Playfair Display', 12),
            foreground='#888888'
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_search_type_selector(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame, text="Search Type:", font=('Playfair Display', 11, 'bold')).pack(side=tk.LEFT)
        ttk.Radiobutton(frame, text="Username", variable=self.search_type, 
                       value="username").pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(frame, text="Email", variable=self.search_type, 
                       value="email").pack(side=tk.LEFT)
    
    def create_input_field(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame, text="Search Query:", font=('Playfair Display', 11, 'bold')).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(
            frame,
            width=50,
            bg=self.secondary_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=('Playfair Display', 10),
            relief=tk.FLAT
        )
        self.search_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
    
    def create_platform_selector(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame, text="Platforms:", font=('Playfair Display', 11, 'bold')).pack(side=tk.LEFT)
        
        # Create a frame for the listbox with a border
        listbox_frame = ttk.Frame(frame)
        listbox_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.platform_listbox = tk.Listbox(
            listbox_frame,
            selectmode=tk.MULTIPLE,
            height=5,
            bg=self.secondary_color,
            fg=self.fg_color,
            selectbackground=self.accent_color,
            selectforeground=self.fg_color,
            font=('Playfair Display', 10),
            relief=tk.FLAT
        )
        self.platform_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Add platforms to listbox
        platforms = ["Twitter", "GitHub", "Instagram", "LinkedIn", "Facebook", "YouTube", "Pinterest"]
        for platform in platforms:
            self.platform_listbox.insert(tk.END, platform)
    
    def create_search_button(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        self.search_button = tk.Button(
            frame,
            text="Search",
            command=self.perform_search,
            bg=self.accent_color,
            fg=self.bg_color,
            font=('Playfair Display', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=5,
            activebackground=self.hover_color,
            activeforeground=self.bg_color
        )
        self.search_button.pack(side=tk.LEFT)
        
        # Add hover effect
        self.search_button.bind('<Enter>', lambda e: self.search_button.configure(bg=self.hover_color))
        self.search_button.bind('<Leave>', lambda e: self.search_button.configure(bg=self.accent_color))
    
    def create_progress_bar(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            frame, 
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=400,
            style='Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=tk.X, expand=True)
        
        self.status_label = ttk.Label(
            frame,
            text="Ready",
            font=('Playfair Display', 10),
            foreground='#888888'
        )
        self.status_label.pack(pady=(5, 0))
    
    def create_results_area(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Create a frame for the results with a border
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            height=20,
            bg=self.secondary_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=('Playfair Display', 10),
            relief=tk.FLAT
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def create_save_button(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X)
        
        self.save_button = tk.Button(
            frame,
            text="Save Results",
            command=self.save_results,
            bg=self.accent_color,
            fg=self.bg_color,
            font=('Playfair Display', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=5,
            activebackground=self.hover_color,
            activeforeground=self.bg_color
        )
        self.save_button.pack(side=tk.LEFT)
        
        # Add hover effect
        self.save_button.bind('<Enter>', lambda e: self.save_button.configure(bg=self.hover_color))
        self.save_button.bind('<Leave>', lambda e: self.save_button.configure(bg=self.accent_color))
    
    def check_queue(self):
        try:
            while True:
                message = self.queue.get_nowait()
                if message['type'] == 'progress':
                    self.update_progress(message['value'], message['status'])
                elif message['type'] == 'result':
                    self.results_text.insert(tk.END, message['text'])
                    self.results_text.see(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self.check_queue)
    
    def update_progress(self, value, status):
        self.progress_var.set(value)
        self.status_label.config(text=status)
    
    def perform_search_thread(self):
        query = self.search_entry.get()
        if not query:
            self.queue.put({'type': 'result', 'text': "Please enter a search query.\n"})
            return
        
        self.queue.put({'type': 'result', 'text': f"Searching for: {query}\n\n"})
        
        if self.search_type.get() == "username":
            platforms = list(usernames.PLATFORMS.keys())
            total_platforms = len(platforms)
            
            for i, platform in enumerate(platforms, 1):
                progress = (i / total_platforms) * 100
                self.queue.put({'type': 'progress', 'value': progress, 'status': f"Checking {platform}..."})
                
                try:
                    # Check the platform
                    platform_results = usernames.check_username(query)
                    data = platform_results.get(platform, {'exists': False, 'url': None, 'profile_info': None})
                    
                    # Show result for this platform
                    if data['exists']:
                        self.queue.put({'type': 'result', 'text': f"[+] Found on {platform}: {data['url']}\n"})
                        if data['profile_info']:
                            # Display common profile info
                            if data['profile_info'].get('name'):
                                self.queue.put({'type': 'result', 'text': f"    Name: {data['profile_info']['name']}\n"})
                            if data['profile_info'].get('bio'):
                                self.queue.put({'type': 'result', 'text': f"    Bio: {data['profile_info']['bio']}\n"})
                            
                            # Platform-specific info
                            if platform == 'Twitter':
                                if data['profile_info'].get('followers'):
                                    self.queue.put({'type': 'result', 'text': f"    Followers: {data['profile_info']['followers']}\n"})
                                if data['profile_info'].get('following'):
                                    self.queue.put({'type': 'result', 'text': f"    Following: {data['profile_info']['following']}\n"})
                            
                            elif platform == 'GitHub':
                                if data['profile_info'].get('latest_repos'):
                                    self.queue.put({'type': 'result', 'text': "    Latest Repositories:\n"})
                                    for repo in data['profile_info']['latest_repos']:
                                        self.queue.put({'type': 'result', 'text': f"      - {repo}\n"})
                            
                            elif platform == 'Instagram':
                                if data['profile_info'].get('followers'):
                                    self.queue.put({'type': 'result', 'text': f"    Followers: {data['profile_info']['followers']}\n"})
                            
                            elif platform == 'LinkedIn':
                                if data['profile_info'].get('headline'):
                                    self.queue.put({'type': 'result', 'text': f"    Headline: {data['profile_info']['headline']}\n"})
                                if data['profile_info'].get('location'):
                                    self.queue.put({'type': 'result', 'text': f"    Location: {data['profile_info']['location']}\n"})
                            
                            elif platform == 'YouTube':
                                if data['profile_info'].get('subscribers'):
                                    self.queue.put({'type': 'result', 'text': f"    Subscribers: {data['profile_info']['subscribers']}\n"})
                                if data['profile_info'].get('latest_videos'):
                                    self.queue.put({'type': 'result', 'text': "    Latest Videos:\n"})
                                    for video in data['profile_info']['latest_videos']:
                                        self.queue.put({'type': 'result', 'text': f"      - {video}\n"})
                            
                            elif platform == 'Pinterest':
                                if data['profile_info'].get('latest_boards'):
                                    self.queue.put({'type': 'result', 'text': "    Latest Boards:\n"})
                                    for board in data['profile_info']['latest_boards']:
                                        self.queue.put({'type': 'result', 'text': f"      - {board}\n"})
                        
                        self.queue.put({'type': 'result', 'text': "\n"})
                    else:
                        self.queue.put({'type': 'result', 'text': f"[-] Not found on {platform}\n\n"})
                    
                    # Minimal delay to show progress
                    time.sleep(0.02)
                    
                except Exception as e:
                    self.queue.put({'type': 'result', 'text': f"Error checking {platform}: {str(e)}\n\n"})
                    time.sleep(0.02)
        else:
            self.queue.put({'type': 'progress', 'value': 50, 'status': "Checking email breaches..."})
            try:
                breaches = email_breach.check_email_breach(query)
                time.sleep(0.05)  # Reduced from 0.1 to 0.05
                
                self.queue.put({'type': 'progress', 'value': 100, 'status': "Search complete"})
                
                if breaches:
                    self.queue.put({'type': 'result', 'text': f"[!] Email found in {len(breaches)} breach(es):\n"})
                    for breach in breaches:
                        self.queue.put({'type': 'result', 'text': f"    - {breach}\n"})
                        time.sleep(0.02)  # Reduced from 0.05 to 0.02
                else:
                    self.queue.put({'type': 'result', 'text': "[✓] No breaches found for this email.\n"})
            except Exception as e:
                self.queue.put({'type': 'result', 'text': f"Error checking email breaches: {str(e)}\n"})
        
        time.sleep(0.05)  # Reduced from 0.1 to 0.05
        self.queue.put({'type': 'progress', 'value': 0, 'status': "Ready"})
    
    def perform_search(self):
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Start search in a separate thread
        search_thread = threading.Thread(target=self.perform_search_thread)
        search_thread.daemon = True
        search_thread.start()
    
    def save_results(self):
        query = self.search_entry.get()
        if not query:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"osint_results_{query}_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(self.results_text.get(1.0, tk.END))
        
        self.results_text.insert(tk.END, f"\nResults saved to: {filename}")

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Using a modern theme
    app = OSINTScoutGUI(root)
    root.mainloop() 