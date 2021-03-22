import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def get_content(full_entry):
    """
    Retrieves a list of the entry's name and infromation.
    """
    entry_info = []
    full_content = [entry.lstrip() for entry in full_entry.replace("#","\n").replace("\r","\n").split("\n") if entry]
    entry_content = full_content[1:]
    entry_info.append(full_content[0])
    entry_info.append(entry_content)
    """
    for entry in full_entry:
        entry_data = [entry_value.lstrip() for entry_value in entry.split("\n",2) if entry_value]
        entry_data = [entry.rstrip() for entry in entry_data if entry]
        entry_data[1] = [entry for entry in entry_data[1].splitlines() if entry]
        entry_info.append(entry_data)
    """

    return entry_info
