import os
from dotenv import load_dotenv

load_dotenv(".env")

DATABASE = "database/database.db"

TOKEN = os.getenv("TOKEN_GITHUB")

OWNER = "Test-robot-0"

REPO = "leetcode"

URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/leetcode-solutions/"

QUESTION_URL = f"https://leetcode.com/problems/"

COOKIES = {
        'csrftoken' : os.getenv("CSRFTOKEN"),
        'LEETCODE_SESSION' : os.getenv("LEETCODE_SESSION"),
}

EXTENSIONS = {
        "python": ".py",
        "python3": ".py",
        "java": ".java",
        "c": ".c",
        "c++": ".cpp",
        "cpp": ".cpp",
        "c#": ".cs",
        "javascript": ".js",
        "typescript": ".ts",
        "go": ".go",
        "kotlin": ".kt",
        "swift": ".swift",
        "rust": ".rs",
        "ruby": ".rb",
        "php": ".php",
        "dart": ".dart",
        "scala": ".scala",
        "elixir": ".ex",
        "erlang": ".erl",
        "racket": ".rkt",
    }
