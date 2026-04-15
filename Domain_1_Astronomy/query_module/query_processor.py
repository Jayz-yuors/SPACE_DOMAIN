import os
from google import genai


class QueryProcessor:
    """
    Lightweight Query Normalizer.

    Responsibilities:
    - Correct spelling and grammar
    - Preserve scientific meaning
    - Never reject valid space-related queries
    - Never classify intent
    """

    def __init__(self):

        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        self.client = genai.Client(api_key=api_key)

    # -----------------------------------------------------
    # PUBLIC METHOD
    # -----------------------------------------------------

    def process(self, user_query: str):

        if not user_query or len(user_query.strip()) < 3:
            return {
                "status": "rejected",
                "reason": "Query too short."
            }

        corrected_query = self._correct_with_gemini(user_query)

        return {
            "status": "accepted",
            "corrected_query": corrected_query
        }

    # -----------------------------------------------------
    # INTERNAL METHODS
    # -----------------------------------------------------

    def _correct_with_gemini(self, query: str):

        prompt = f"""
Correct the spelling and grammar of the following space-related query.
Do NOT add explanations.
Do NOT interpret.
Do NOT summarize.
Return only the corrected query exactly.

User Query:
{query}
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            corrected = response.text.strip()

            # Safety fallback if Gemini adds extra text
            if len(corrected.split("\n")) > 1:
                corrected = corrected.split("\n")[0].strip()

            return corrected

        except Exception:
            # If Gemini fails, fallback to original query
            return query.strip()