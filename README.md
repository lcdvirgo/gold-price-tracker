# Gold Price Scraper

Automated web scraper that collects gold prices from goldprice.org every 5 minutes using GitHub Actions (100% free).

## 📊 Data Collection

- **Frequency**: Every 5 minutes
- **Source**: https://goldprice.org
- **Storage**: CSV file in `/data` directory
- **Cost**: $0 (uses GitHub Actions free tier)

## 🚀 Setup Instructions

### 1. Create GitHub Repository

```bash
# Create a new repository on GitHub (public or private)
# Clone it to your local machine
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Add Files to Repository

Copy these files to your repository:
- `scraper.py` (the scraper script)
- `.github/workflows/scrape.yml` (the automation workflow)

```bash
# Create directory structure
mkdir -p .github/workflows
mkdir -p data

# Copy the files (assuming they're in the same directory)
# Then add and commit
git add .
git commit -m "Initial commit: Add gold price scraper"
git push origin main
```

### 3. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click on the **"Actions"** tab
3. If prompted, enable GitHub Actions
4. You should see the "Scrape Gold Price" workflow

### 4. Test the Scraper

You can manually trigger the workflow:
1. Go to **Actions** tab
2. Click on **"Scrape Gold Price"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait a few seconds and refresh

### 5. Verify Data Collection

After the first run:
1. Go to your repository
2. Check the `/data` folder
3. You should see `gold_prices.csv` with the scraped data

## 📁 Data Format

The CSV file contains:
- `timestamp`: When the data was scraped (YYYY-MM-DD HH:MM:SS)
- `price`: Gold price in USD per oz
- `url`: Source URL
- `status`: Scraping status (success/error)

Example:
```csv
timestamp,price,url,status
2025-12-13 10:00:00,4300.40,https://goldprice.org,success
2025-12-13 10:05:00,4301.15,https://goldprice.org,success
```

## ⚙️ Configuration

### Change Scraping Frequency

Edit `.github/workflows/scrape.yml`:

```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
  # - cron: '*/10 * * * *'  # Every 10 minutes
  # - cron: '0 * * * *'     # Every hour
  # - cron: '0 0 * * *'     # Once daily at midnight
```

### Customize Data Extraction

Edit `scraper.py` to extract additional data like:
- Silver prices
- Price changes
- Percentage changes
- Different currencies

## 🔍 Troubleshooting

### Workflow Not Running?

1. Check if Actions are enabled in repository settings
2. Ensure the workflow file is in `.github/workflows/`
3. Check the Actions tab for error messages

### No Data Being Saved?

1. Check the workflow logs in Actions tab
2. Look for Python errors in the scraper output
3. Website structure might have changed (update selectors)

### Rate Limiting?

GitHub Actions has limits:
- Public repos: Unlimited (within reason)
- Private repos: 2,000 minutes/month (more than enough for 5-min intervals)

## 📈 Viewing Your Data

### Download CSV
1. Navigate to `/data/gold_prices.csv` in your repo
2. Click "Download" or "Raw"

### Visualize Data
You can use:
- Google Sheets: Import the CSV
- Excel: Open the CSV file
- Python/Pandas: Analyze programmatically

### Create a Dashboard
Add a simple viewer by creating `index.html`:
- Use GitHub Pages to host
- Display latest price and chart
- Fully free static hosting

## 💡 Pro Tips

1. **Keep History**: GitHub automatically versions your data
2. **Add Alerts**: Use GitHub Actions to send emails/notifications when price changes significantly
3. **Export to Google Sheets**: Use GitHub Actions + Google Sheets API
4. **Monitor Uptime**: Check Actions tab regularly

## 🆓 Cost Breakdown

- **GitHub Actions**: $0 (free tier)
- **Data Storage**: $0 (included in repo)
- **Bandwidth**: $0 (minimal scraping)
- **Total Monthly Cost**: **$0.00**

## 📝 License

Free to use and modify!

---

**Happy Scraping! 📊💰**
