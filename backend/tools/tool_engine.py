import subprocess
import requests


def run_python(code):

    try:

        result = subprocess.check_output(
            ["python", "-c", code],
            stderr=subprocess.STDOUT
        )

        return result.decode()

    except Exception as e:
        return str(e)


def web_search(query):

    url = f"https://duckduckgo.com/?q={query}"

    return f"Search results available at: {url}"


def analyze_text(text):

    word_count = len(text.split())

    return {
        "word_count": word_count,
        "summary": text[:300]
    }