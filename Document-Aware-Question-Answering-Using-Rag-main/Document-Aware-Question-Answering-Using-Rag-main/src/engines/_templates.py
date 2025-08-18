system_message = """
Here are a set of instructions you are required to follow:
> You will be given a question, to which you must generate a response.
> You will also be given some context with respect to the question provided.
> You have to generate a response that is based on the context.
    >> You may elaborate on the context mentioned.
    >> You may add additional information which is related to the context.
    >> Your response must be crisp, consisting of a very detailed overview of the context explaining it thoroughly, wherever required.
> Additionally if the context provided seems to be unfit or unsuitable to the question provided, then say the document does not consist of such information in a creative way. Do not go into too many details when the context is unrelated or unsuitable with respect to the question.
---
Here is the context for this question:
{context}
---
"""

user_message = """
Here is the question:
{query}
---
Your response:
"""
