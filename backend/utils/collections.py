# # utils/collections.py
#
# def build_collection_name(subject: str, topic: str) -> str:
#     """
#     Standardizes collection names for ChromaDB.
#     Converts subject+topic into lowercase, underscores instead of spaces.
#     """
#     return f"{subject.strip().lower()}_{topic.strip().lower()}".replace(" ", "_")
# utils/collections.py
def make_collection_name(class_name: str, subject: str, topic: str) -> str:
    """Standardize how collection names are built"""
    return f"{class_name}_{subject}_{topic}".replace(" ", "_").lower()
