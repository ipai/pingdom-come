# Pingdom Come (Delivers too!)
A system that aggregates data from multiple sources (Cloudflare, Vercel, GitHub, Chrome Web Store) and sends daily/weekly reports with key metrics via Temporal.

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL:
   - Create a new PostgreSQL database named `pingdom_db`
   - Copy `.env.example` to `.env` and update the database credentials

4. Run the application:
   ```bash
   python app.py
   ```

The application will be available at http://localhost:5000
