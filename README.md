# Simple AI agent practice

# Requirements

Gemini API - gemini-2.5-flash
https://ai.google.dev/gemini-api/docs/pricing

Until recently, Google offered generous free-tier limits on the Gemini API – including for gemini-2.5-flash, the model we recommend for this project. However, in December 2025 Google drastically lowered the free-tier rate limits, making it difficult to complete this project without hitting the limits often.

It seems Gemini API pricing will continue to change frequently and without notice. We recommend, if possible, setting up a paid account with Google and using the gemini-2.5-flash model. You should accrue no more than ~$1–2 in charges during this course. Otherwise, you can still use gemini-2.5-flash on the free tier, but you'll be subject to very few requests per day

WSL2 for windows
Python 3.10+
The uv project/package manager [installation docs](https://docs.astral.sh/uv/getting-started/installation/)

# Example

Manually update calculator/pkg/calculator.py and change the precedence of the + operator value to 3.
Run the calculator app, to make sure it's now producing incorrect results: uv run calculator/main.py "3 + 7 * 2" (this should be 17, but because we broke it, it will return 20).
> uv run calculator/main.py "3 + 7 * 2"
Run your agent and ask it, "Fix the bug: 3 + 7 * 2 shouldn't be 20."

> uv run main.py "fix my calculator app, it's not starting correctly"
# Calling function: get_files_info
# Calling function: get_file_content
# Calling function: write_file
# Calling function: run_python_file
# Calling function: write_file
# Calling function: run_python_file
# Final response:
# Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way.