import re
import ollama

# =========================================================
# FIXED MODEL
# =========================================================

MODEL_NAME = "qwen2.5:1.5b"


# =========================================================
# LANGUAGE DETECTION
# =========================================================

def detect_language(text):

    if re.search(r'[\u0900-\u097F]', text):

        hindi_words = [
            "क्या", "कौन", "कहाँ", "कैसे", "है", "हैं"
        ]

        marathi_words = [
            "काय", "कोण", "कुठे", "कसे", "आहे"
        ]

        hindi_score = sum(1 for w in hindi_words if w in text)
        marathi_score = sum(1 for w in marathi_words if w in text)

        if hindi_score > marathi_score:
            return "Hindi"

        return "Marathi"

    return "English"


# =========================================================
# CLEAN RESPONSE
# =========================================================

def clean_response(text):

    # Remove HTML
    text = re.sub(r"<[^>]*>", "", text)

    # Remove markdown
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)

    # Remove repeated empty lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# =========================================================
# DOCUMENT CLEANER
# =========================================================

def clean_document(text):

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove strange OCR characters
    text = re.sub(r"[^\w\s\.\,\-\@\:\n\/\(\)\u0900-\u097F]", "", text)

    return text[:12000]


# =========================================================
# MAIN FUNCTION
# =========================================================

def ask_llm(context, question, language="English"):

    try:

        # Clean PDF text
        context = clean_document(context)

        # Auto detect language from question
        detected_lang = detect_language(question)

        if detected_lang != "English":
            language = detected_lang

        # Fallback messages
        fallback = {
            "English": "Answer not found in document.",
            "Hindi": "दस्तावेज़ में उत्तर नहीं मिला।",
            "Marathi": "या कागदपत्रात उत्तर सापडले नाही."
        }

        not_found = fallback.get(language)

        # Language rules
        if language == "Marathi":

            instruction = f"""
            प्रश्नाचे उत्तर मराठीत द्या.

            फक्त दस्तावेजातील माहिती वापरा.

            माहिती नसेल तर:
            "{not_found}"

            HTML वापरू नका.
            Markdown वापरू नका.
            उत्तर छोटे आणि स्पष्ट द्या.
            """

        elif language == "Hindi":

            instruction = f"""
            प्रश्न का उत्तर हिंदी में दें।

            केवल दस्तावेज़ की जानकारी का उपयोग करें।

            जानकारी नहीं मिलने पर:
            "{not_found}"

            HTML का उपयोग न करें।
            Markdown का उपयोग न करें।
            उत्तर छोटा और स्पष्ट रखें।
            """

        else:

            instruction = f"""
            Answer only from the document.

            If answer not found say:
            "{not_found}"

            Do not use HTML.
            Do not use markdown.
            Keep answer clear and short.
            """

        # Final Prompt
        prompt = f"""
        DOCUMENT:
        {context}

        QUESTION:
        {question}

        RULES:
        {instruction}
        """

        # Ollama response
        response = ollama.chat(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            options={
                "temperature": 0.1,
                "num_predict": 300
            }

        )

        answer = response["message"]["content"]

        answer = clean_response(answer)

        if not answer.strip():
            return not_found

        return answer

    except ollama.ResponseError as e:

        return f"Model Error: {str(e)}"

    except Exception as e:

        return f"Error: {str(e)}"

