from transformers import pipeline

qa = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)


def answer_question(context, question):

    try:
        result = qa(
            question=question,
            context=context[:3000]
        )

        return result["answer"]

    except:
        return "Could not find clear answer."