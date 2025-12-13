import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import re

def scrape_gold_price():
    """Scrape current gold price from goldprice.org"""
    url = "https://goldprice.org"
    
    try:
        # Add headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Try multiple methods to find the gold price
        price = None
        change = None
        percent_change = None
        
        # Method 1: Look for meta tags with price data
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            content = meta.get('content', '')
            if 'gold' in content.lower() and re.search(r'\d{4}', content):
                match = re.search(r'(\d{1},?\d{3}\.\d{1,2})', content)
                if match:
                    price = match.group(1)
                    break
        
        # Method 2: Look in script tags for JSON data
        if not price:
            scripts = soup.find_all('script')
            for script in scripts:
                script_text = script.string if script.string else ''
                # Look for price patterns in JavaScript
                match = re.search(r'"price["\']?\s*:\s*["\']?(\d{1},?\d{3}\.\d{1,2})', script_text)
                if match:
                    price = match.group(1)
                    break
        
        # Method 3: Search page text for price patterns near "Gold Price" or "USD"
        if not price:
            page_text = soup.get_text()
            lines = page_text.split('\n')
            
            for i, line in enumerate(lines):
                # Look for lines containing "Gold" or near USD markers
                if 'gold' in line.lower() or 'usd' in line.lower():
                    # Search this line and nearby lines for price patterns
                    search_text = ' '.join(lines[max(0, i-2):min(len(lines), i+3)])
                    match = re.search(r'(\d{1},\d{3}\.\d{1,2})', search_text)
                    if match:
                        price = match.group(1)
                        break
        
        # Method 4: Look for any large dollar amount (gold is typically $2000-$5000)
        if not price:
            all_numbers = re.findall(r'(\d{1},\d{3}\.\d{1,2})', soup.get_text())
            for num in all_numbers:
                # Convert to float for range check
                num_value = float(num.replace(',', ''))
                if 2000 <= num_value <= 5000:
                    price = num
                    break
        
        return {
            'timestamp': timestamp,
            'price': price if price else 'N/A',
            'change': change if change else 'N/A',
            'percent_change': percent_change if percent_change else 'N/A',
            'url': url,
            'status': 'success' if price else 'parsing_failed'
        }
        
    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {
            'timestamp': timestamp,
            'price': 'ERROR',
            'change': 'ERROR',
            'percent_change': 'ERROR',
            'url': url,
            'status': f'error: {str(e)}'
        }

def save_to_csv(data):
    """Append data to CSV file"""
    csv_file = 'data/gold_prices.csv'
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Check if file exists to determine if we need headers
    file_exists = os.path.isfile(csv_file)
    
    # Append to CSV
    with open(csv_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'price', 'change', 'percent_change', 'url', 'status'])
        
        # Write header if file is new
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)
    
    print(f"Data saved: {data}")

if __name__ == "__main__":
    print("Scraping gold price from goldprice.org...")
    data = scrape_gold_price()
    save_to_csv(data)
    print(f"Latest gold price: ${data['price']} at {data['timestamp']}")
