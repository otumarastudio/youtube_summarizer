# 📺 YouTube Video Summarizer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/your-username/youtube-video-summarizer)](https://github.com/your-username/youtube-video-summarizer/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/your-username/youtube-video-summarizer)](https://github.com/your-username/youtube-video-summarizer/pulls)

The YouTube Video Summarizer is a powerful Python-based tool that harnesses the capabilities of artificial intelligence to automatically generate concise and informative summaries of YouTube videos. 🚀

## 🌟 Features

- 🎥 Extracts video content and metadata from YouTube videos
- ✂️ Splits the video content into manageable chunks
- 🧠 Generates concise summaries for each chunk using state-of-the-art AI techniques
- 📋 Combines the summaries into a comprehensive report
- 📝 Saves the report as a Markdown file for easy readability and sharing

## 🛠️ Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/youtube-video-summarizer.git
   ```

2. Navigate to the project directory:
   ```
   cd youtube-video-summarizer
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - For Windows:
     ```
     venv\Scripts\activate
     ```
   - For macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Set up the OpenAI API key:
   - Create a `.env` file in the project root directory
   - Add the following line to the `.env` file, replacing `YOUR_API_KEY` with your actual OpenAI API key:
     ```
     OPENAI_API_KEY=YOUR_API_KEY
     ```

## 🚀 Usage

1. Make sure you have activated the virtual environment (see [Installation](#%EF%B8%8F-installation) step 4).

2. Run the program:
   ```
   python main.py
   ```

3. When prompted, enter the YouTube video URL you want to summarize.

4. Optionally, you can enter an additional prompt to guide the summary generation.

5. The program will process the video, generate summaries, and save the final report as a Markdown file in the `summary_result` directory.

6. Open the generated Markdown file to view the video summary. 📖
   

## 🤝 Contributing

Contributions are welcome! 🙌 If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. Make sure to follow the [contribution guidelines](CONTRIBUTING.md).

## 📄 License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as per the terms of the license.



Let's make video summarization easier and more accessible together! 🎉
