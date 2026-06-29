from openai import OpenAI
from pathlib import Path
import json
import sys
import re

# Initialize client with your API key
with open("PATH/chat_gpt_api_key", "r") as f:
    gpt_key = f.read()

client = OpenAI(api_key=gpt_key)


def validate_commented_text(data: dict) -> None:
    """
    Checks that the input JSON has the expected structure.

    Expected format:
    {
        "title" : "",
        "original_text": "...",
        "comments": [
            {
                "comment": "...",
                "anchor_text": "..."
            }
        ]
    }
    """

    if not isinstance(data, dict):
        raise ValueError("The JSON root must be a dictionary.")

    if "original_text" not in data:
        raise ValueError("Missing key: original_text")

    if "comments" not in data:
        raise ValueError("Missing key: comments")


    if not isinstance(data["original_text"], str):
        raise ValueError("original_text must be a string.")

    if not isinstance(data["comments"], list):
        raise ValueError("comments must be a list.")

    for i, comment in enumerate(data["comments"]):
        if not isinstance(comment, dict):
            raise ValueError(f"Comment {i} must be a dictionary.")

        if "comment" not in comment:
            raise ValueError(f"Comment {i} is missing key: comment")

        if "anchor_text" not in comment:
            raise ValueError(f"Comment {i} is missing key: anchor_text")

        if not isinstance(comment["comment"], str):
            raise ValueError(f"Comment {i}: comment must be a string.")

        if not isinstance(comment["anchor_text"], str):
            raise ValueError(f"Comment {i}: anchor_text must be a string.")


def integrate_comments_with_openai(input_json_path: str, output_txt_path: str) -> str:
    """
    Reads a commented_text JSON file, uploads it to OpenAI,
    and returns a revised text that integrates the comments.
    """

    input_path = Path(input_json_path)
    output_path = Path(output_txt_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_json_path}")


    with open(input_path, "r", encoding="utf-8") as f:
        #content = purge_ids_from_text(f)
        #commented_text = json.load(content)
        commented_text = json.load(f)
    
    validate_commented_text(commented_text)

    # Upload the JSON file so the model can use it as file input.
    uploaded_file = client.files.create(
        file=open(input_path, "rb"),
        purpose="user_data"
    )

    instructions = """
You are an expert editor.

You will receive a JSON file with this structure:

{
    "title" : "",
    "original_text": "...",
    "comments": [
        {
            "comment": "...",
            "anchor_text": "..."
        }
    ]
}

Your task:
Rewrite the original_text into a new, polished version that integrates the information from the comments.

Rules:
1. Preserve the meaning and structure of the original text as much as possible.
2. If a comment has anchor_text, use that anchor_text to decide where the comment should be integrated.
3. If anchor_text is empty, missing, or does not exactly appear in the original text, integrate the comment naturally wherever it best fits.
4. Do not mention that there were comments.
5. Do not output explanations.
6. Do not output JSON.
7. Output only the final revised text.
8. Use proper syntax, grammar, paragraph structure, and natural style.
9. If a comment contradicts the original text, prefer a cautious rewrite that avoids unsupported certainty.
10. If a comment is unclear, integrate only the useful part without inventing details.
11. Preserve the language of the original text
"""

    response = client.responses.create(
        model="gpt-5",
        instructions=instructions,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": uploaded_file.id
                    },
                    {
                        "type": "input_text",
                        "text": "Please integrate the comments into the original text and return only the revised text."
                    }
                ]
            }
        ]
    )

    revised_text = response.output_text

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(revised_text)

    return revised_text

