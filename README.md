# UdaPlay - AI Game Research Agent Project

## Project Scenario

You’ve been hired as an AI Engineer at a gaming analytics company developing an assistant called UdaPlay. Executives, analysts, and gamers want to ask natural language questions like:

- “Who developed FIFA 21?”
- “When was God of War Ragnarok released?”
- “What platform was Pokémon Red launched on?”
- “What is Rockstar Games working on right now?”

Your agent should:

1. Attempt to answer the question from internal knowledge (about a pre-loaded list of companies and games)
2. If the information is not found or confidence is low, search the web
3. Parse and persist the information in long-term memory
4. Generate a clean, structured answer/report

## Project Specifications

In this project, you will build an AI Research Agent called UdaPlay designed to answer questions about video games. The agent will be capable of:

- Answering user questions about games, including:
  - Game titles and their details
  - Release dates and platforms
  - Game descriptions and genres
  - Publisher information
- Using a two-tier information retrieval system:
  - Primary: RAG (Retrieval Augmented Generation) over a local dataset of games
  - Secondary: Web search using the Tavily API when internal knowledge is insufficient
- Implementing a robust evaluation system:
  - Assessing the quality of retrieved information
  - Determining when to fall back to web search
  - Providing confidence levels in answers
- Generating clear, well-structured responses that:
  - Cite information sources
  - Combine information from multiple sources when needed
  - Present information in a natural, readable format

## Project Overview
UdaPlay is an AI-powered research agent for the video game industry. This project is divided into two main parts that will help you build a sophisticated AI agent capable of answering questions about video games using both local knowledge and web searches.

## Project Structure

### Part 1: Offline RAG (Retrieval-Augmented Generation)
In this part, you'll build a Vector Database using ChromaDB to store and retrieve video game information efficiently.

Key tasks:
- Set up ChromaDB as a persistent client
- Create a collection with appropriate embedding functions
- Process and index game data from JSON files
- Each game document contains:
  - Name
  - Platform
  - Genre
  - Publisher
  - Description
  - Year of Release

### Part 2: AI Agent Development
Build an intelligent agent that combines local knowledge with web search capabilities.

The agent will have the following capabilities:
1. Answer questions using internal knowledge (RAG)
2. Search the web when needed
3. Maintain conversation state
4. Return structured outputs
5. Store useful information for future use

Required Tools to Implement:
1. `retrieve_game`: Search the vector database for game information
2. `evaluate_retrieval`: Assess the quality of retrieved results
3. `game_web_search`: Perform web searches for additional information

## Requirements

### Environment Setup
Create a `.env` file with the following API keys:
```
OPENAI_API_KEY="YOUR_KEY"
CHROMA_OPENAI_API_KEY="YOUR_KEY"
TAVILY_API_KEY="YOUR_KEY"
```

### Project Dependencies
- Python 3.11+
- ChromaDB
- OpenAI
- Tavily
- dotenv

### Directory Structure
```
project/
├── starter/
│   ├── games/           # JSON files with game data
│   ├── lib/             # Custom library implementations
│   │   ├── llm.py       # LLM abstractions
│   │   ├── messages.py  # Message handling
│   │   ├── ...
│   │   └── tooling.py   # Tool implementations
│   ├── Udaplay_01_starter_project.ipynb  # Part 1 implementation
│   └── Udaplay_02_starter_project.ipynb  # Part 2 implementation
```

## Getting Started

1. Run the setup script to create a virtual environment and install all
   dependencies:
   - On Linux/macOS: `./setup_linux.sh`
   - On Windows: `setup_windows.bat`
2. Set up your `.env` file with necessary API keys
3. Follow the notebooks in order:
   - Complete Part 1 to set up your vector database
   - Complete Part 2 to implement the AI agent

## Testing Your Implementation

After completing both parts, test your agent with questions like:
- "When was Pokémon Gold and Silver released?"
- "Which one was the first 3D platformer Mario game?"
- "Was Mortal Kombat X released for PlayStation 5?"

## Advanced Features

After completing the basic implementation, you can enhance your agent with:
- Long-term memory capabilities
- Additional tools and capabilities

## Notes
- Make sure to implement proper error handling
- Follow best practices for API key management
- Document your code thoroughly
- Test your implementation with various types of queries
