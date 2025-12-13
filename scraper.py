import requests
from datetime import datetime
import pytz
import csv
import os
import json

def scrape_gold_price():
    """Fetch current gold price from a reliable API"""
    sg_tz = pytz.timezone('Asia/Singapore')
    timestamp = datetime.now(sg_tz).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    # Try multiple sources for gold price
    
    # Method 1: GoldAPI.io (free tier available)
    try:
        # Using metals-api.com free endpoint
        url = "https://api.metals.dev/v1/latest?api_key=demo&base=USD&currencies=XAU"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # XAU is gold in troy ounces, we need to convert
            # Price is given as USD per XAU, we want XAU per USD (price of gold)
            if 'rates' in data and 'XAU' in data['rates']:
                xau_rate = data['rates']['XAU']
                # Convert: 1 USD = xau_rate XAU, so 1 XAU = 1/xau_rate USD
                gold_price = round(1 / xau_rate, 2)
                
                return {
                    'timestamp': timestamp,
                    'price': f"{gold_price:,.2f}",
                    'change': 'N/A',
                    'percent_change': 'N/A',
                    'url': 'https://api.metals.dev',
                    'status': 'success'
                }
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    # Method 2: Try goldprice.org JSON endpoint
    try:
        url = "https://data-asg.goldprice.org/dbXRates/USD"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # The response structure varies, try to find gold price
            if 'items' in data:
                for item in data['items']:
                    if item.get('curr') == 'USD':
                        price = item.get('xauPrice')
                        if price:
                            return {
                                'timestamp': timestamp,
                                'price': f"{float(price):,.2f}",
                                'change': item.get('chgXau', 'N/A'),
                                'percent_change': item.get('pcXau', 'N/A'),
                                'url': 'https://goldprice.org',
                                'status': 'success'
                            }
    except Exception as e:
        print(f"Method 2 failed: {e}")
    
    # Method 3: Alternative free API
    try:
        # Using free forex API that includes gold (XAU)
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Note: This API might not have gold, but worth trying
            if 'rates' in data and 'XAU' in data['rates']:
                xau_rate = data['rates']['XAU']
                gold_price = round(1 / xau_rate, 2)
                
                return {
                    'timestamp': timestamp,
                    'price': f"{gold_price:,.2f}",
                    'change': 'N/A',
                    'percent_change': 'N/A',
                    'url': 'https://api.exchangerate-api.com',
                    'status': 'success'
                }
    except Exception as e:
        print(f"Method 3 failed: {e}")
    
    # Method 4: Try a different approach - scrape the mobile version
    try:
        url = "https://goldprice.org/gold-price-usa.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            import re
            # Look for price patterns in the HTML
            text = response.text
            
            # Try to find gold price pattern
            patterns = [
                r'gold.*?(\d{1},\d{3}\.\d{2})',
                r'usd.*?(\d{1},\d{3}\.\d{2})',
                r'price.*?(\d{1},\d{3}\.\d{2})',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    price = match.group(1)
                    # Validate it's in reasonable gold price range
                    price_val = float(price.replace(',', ''))
                    if 1500 <= price_val <= 6000:
                        return {
                            'timestamp': timestamp,
                            'price': price,
                            'change': 'N/A',
                            'percent_change': 'N/A',
                            'url': url,
                            'status': 'success'
                        }
    except Exception as e:
        print(f"Method 4 failed: {e}")
    
    # If all methods fail
    return {
        'timestamp': timestamp,
        'price': 'N/A',
        'change': 'N/A',
        'percent_change': 'N/A',
        'url': 'multiple sources',
        'status': 'all_methods_failed'
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
    print("Fetching gold price from multiple sources...")
    data = scrape_gold_price()
    save_to_csv(data)
    print(f"Latest gold price: ${data['price']} at {data['timestamp']}")
    print(f"Status: {data['status']}")
