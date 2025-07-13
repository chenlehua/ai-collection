from typing import Final
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API key for authentication
API_KEY: Final = os.getenv("MCP_API_KEY", "your_super_secret_key_123")
