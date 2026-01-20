def handle_identity_and_trick_questions(message: str) -> str | None:
    """
    Detect trick / identity / hallucination-prone questions.
    Return a safe response if detected, else None.
    """

    msg = message.lower()

    identity_questions = [
        "are you a bot",
        "are you an ai",
        "what model are you",
        "what ai are you",
        "who made you",
        "who built you",
    ]

    impossible_memory = [
        "did you see me",
        "remember that secret",
        "what did you say yesterday",
        "do you remember last week",
        "have we met before",
    ]

    appearance_questions = [
        "what do i look like",
        "how do i look",
        "describe my face",
    ]

    for q in identity_questions:
        if q in msg:
            return (
                "I’m just someone you can talk to freely here — "
                "no labels, no tech talk. What’s on your mind?"
            )

    for q in impossible_memory:
        if q in msg:
            return (
                "I only remember things you choose to share with me here. "
                "If you want, you can remind me again."
            )

    for q in appearance_questions:
        if q in msg:
            return (
                "I don’t have a way to see you, but if you want to describe yourself, "
                "I’m happy to listen."
            )

    return None
