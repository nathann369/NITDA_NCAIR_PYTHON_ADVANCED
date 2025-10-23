class DiaryLockedError(Exception):
    """Raised when trying to access a locked diary."""
    pass

class EntryNotFoundError(Exception):
    """Raised when an entry is not found."""
    pass
