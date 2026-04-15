import json
import requests


class AILabellingEngine:

    def __init__(self, model_name="phi"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"

    # -----------------------------------------------------
    # MAIN METHOD
    # -----------------------------------------------------

    def label_image(self, image, scientific_context=None):

        filtered_context = self._filter_context(scientific_context)

        if not filtered_context:
            return self._empty_response("No scientific context provided.")

        prompt = self._build_prompt(filtered_context)

        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",  # Force strict JSON
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 1500,   # 🔥 Long-form generation
                        "top_p": 0.9,
                        "repeat_penalty": 1.1
                    }
                },
                timeout=300  # Increased timeout for long responses
            )

            response.raise_for_status()

            raw_text = response.json().get("response", "").strip()

            if not raw_text:
                return self._empty_response("Model returned empty response.")

            try:
                return json.loads(raw_text)

            except json.JSONDecodeError:
                return {
                    "error": "Model returned invalid JSON",
                    "raw_response": raw_text
                }

        except requests.exceptions.Timeout:
            return self._empty_response("Ollama timed out during long-form generation.")

        except Exception as e:
            return {
                "error": "Ollama API call failed",
                "details": str(e)
            }

    # -----------------------------------------------------
    # FILTER CONTEXT (REMOVE HEAVY DATA)
    # -----------------------------------------------------

    def _filter_context(self, scientific_context):

        if not scientific_context:
            return {}

        return {
            "quantitative_metrics": scientific_context.get("quantitative_metrics"),
            "morphological_metrics": scientific_context.get("morphological_metrics"),
            "space_metrics": scientific_context.get("space_metrics"),
            "segmentation_metrics": scientific_context.get("segmentation_metrics")
        }

    # -----------------------------------------------------
    # BUILD LONG-FORM SCIENTIFIC PROMPT
    # -----------------------------------------------------

    def _build_prompt(self, filtered_context):

        return f"""
You are a professional astrophysicist performing a deep scientific interpretation of computed astronomical image metrics.

Write a highly detailed, technically rigorous scientific analysis in well-structured paragraphs.

The response must:

- Classify the likely astronomical scene
- Interpret stellar population metrics
- Analyze radiative and emission properties
- Explain morphological structure
- Infer underlying physical processes
- Discuss possible astrophysical mechanisms
- Evaluate uncertainty and limitations
- Avoid mentioning telescopes, instruments, or missions
- Base reasoning strictly on provided metrics
- Maintain formal scientific tone

Write between 25 and 50 sentences.
Use cohesive academic-style paragraph formatting.

Metrics:
{json.dumps(filtered_context)}

Respond in STRICT JSON format:

{{
  "scientific_summary": ""
}}
"""

    # -----------------------------------------------------
    # SAFE EMPTY RESPONSE
    # -----------------------------------------------------

    def _empty_response(self, message):

        return {
            "scientific_summary": message
        }