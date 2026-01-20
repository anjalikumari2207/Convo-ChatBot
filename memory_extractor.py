def extract_user_memory(message: str) -> dict:
    """
    Extract structured memory from user message.
    ONLY stores info explicitly stated by the user.
    """

    message_lower = message.lower()
    memory = {}

    # Name extraction
    if "my name is" in message_lower:
        memory["name"] = message.split("is")[-1].strip()

    # Interests extraction
    if "i like" in message_lower:
        memory["interests"] = message.split("like")[-1].strip()

    # Mood extraction
    if "i feel" in message_lower:
        memory["mood"] = message.split("feel")[-1].strip()

    return memory
