import os
import google.generativeai as genai
import requests
from dotenv import load_dotenv

# Load API keys
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Define the model once
model = genai.GenerativeModel('gemini-2.5-flash')

def reconstruct_text(fragment):
    prompt = f"Reconstruct the intended meaning of this message: {fragment}"
    response = model.generate_content(prompt)
    return response.text  # ✅ correct and inside the function

def search_web(query):
    """Search the web using SerpAPI."""
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 5
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    results = []
    if "organic_results" in data:
        for item in data["organic_results"][:5]:
            results.append(item.get("link", ""))
    return results

def generate_report(original, reconstructed, links):
    """Create the final reconstruction report."""
    report = "--- RECONSTRUCTION REPORT ---\n\n"
    report += "[Original Fragment]\n" + original + "\n\n"
    report += "[AI-Reconstructed Text]\n" + reconstructed + "\n\n"
    report += "[Contextual Sources]\n"
    for link in links:
        report += f"- {link}\n"
    return report

def main():
    print("Project Chronos: The AI Archeologist \n")
    fragment = input("Enter the fragmented text: ")
    print("\nReconstructing using Gemini...")
    reconstructed = reconstruct_text(fragment)
    print("\nSearching the web for context...")
    links = search_web(reconstructed)
    report = generate_report(fragment, reconstructed, links)
    print("\n" + report)

    with open("Reconstruction_Report.txt", "w") as f:
        f.write(report)
    print("\nReport saved as 'Reconstruction_Report.txt'")

if __name__ == "__main__":
    main()
