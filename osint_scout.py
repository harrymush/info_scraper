from colorama import Fore, Style, init
init(autoreset=True)

import argparse
from modules import usernames, email_breach
import os
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="OSINT Scout: Find usernames and emails across platforms")
    parser.add_argument('--username', help='Username to search for')
    parser.add_argument('--email', help='Email to check for breaches')
    args = parser.parse_args()

    if not args.username and not args.email:
        print(f"{Fore.YELLOW}No username or email provided. Use --username <username> or --email <email>")
        return

    results = {}
    if args.username:
        print(f"{Fore.CYAN}[*] Searching for username '{args.username}' across platforms...")
        results = usernames.check_username(args.username)
        for platform, url in results.items():
            if url:
                print(f"{Fore.GREEN}[+] Found on {platform}: {url}")
            else:
                print(f"{Fore.RED}[-] Not found on {platform}")

    if args.email:
        print(f"{Fore.CYAN}[*] Checking breach status for '{args.email}'...")
        breaches = email_breach.check_email_breach(args.email)
        if breaches:
            print(f"{Fore.RED}[!] Email found in {len(breaches)} breach(es):")
            for breach in breaches:
                print(f"    - {breach}")
        else:
            print(f"{Fore.GREEN}[✓] No breaches found for this email.")

    if results or args.email:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"osint_results_{args.username or args.email}_{timestamp}.txt"
        with open(filename, "w") as f:
            if args.username:
                f.write(f"Results for username: {args.username}\n\n")
                for platform, url in results.items():
                    if url:
                        f.write(f"[+] Found on {platform}: {url}\n")
                    else:
                        f.write(f"[-] Not found on {platform}\n")
            
            if args.email:
                f.write(f"\nBreach check for: {args.email}\n")
                if breaches:
                    for breach in breaches:
                        f.write(f"[!] Found in breach: {breach}\n")
                else:
                    f.write("[✓] No breaches found\n")

        print(f"\n{Fore.MAGENTA}[+] Results saved to: {filename}")

if __name__ == '__main__':
    main()