# --------------------------------
# In-Memory Conversation Store
# --------------------------------

conversation_memory = []


# --------------------------------
# Add Message
# --------------------------------

def add_to_memory(role, content):

    conversation_memory.append({

        "role": role,

        "content": content
    })


# --------------------------------
# Get Memory
# --------------------------------

def get_memory():

    return conversation_memory[-6:]


# --------------------------------
# Clear Memory
# --------------------------------

def clear_memory():

    conversation_memory.clear()