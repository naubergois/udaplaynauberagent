from dotenv import load_dotenv
import os

if not load_dotenv():
    load_dotenv('config.env')
assert os.getenv('OPENAI_API_KEY') is not None
assert os.getenv('TAVILY_API_KEY') is not None
