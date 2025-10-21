Video Search Engine
Overview
This project implements a search engine that searches inside videos based on their content. It leverages cutting-edge AI models and tools to analyze video scenes, extract captions, and enable text-based and AI-assisted search capabilities.

Features
Download YouTube videos using yt-dlp.
Detect scenes in the video using pyscenedetect.
Extract captions for each scene using the Moondream2 image-to-text model.
Store scene captions in scene_captions.json to avoid redundant processing.
Search scenes using text queries:
Simple string matching (str.find or in).
Enhanced fuzzy matching using rapidfuzz.
Display search results by creating a collage of matching scenes.
Auto-complete search queries using prompt_toolkit.
Support video-based search using Google Gemini's multi-modal model.
