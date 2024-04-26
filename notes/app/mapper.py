from internet import get_author_login_by_id
from schemas import NoteReadUnauthorized, NoteRead


async def mapper_node_to_note_unauthorized(note):
    author_login = await get_author_login_by_id(note.author_id)
    note_read = NoteReadUnauthorized(title=note.title, content=note.content, author_login=author_login)
    return note_read


async def mapper_note_to_noteread(current_user_id, note):
    author_login = await get_author_login_by_id(note.author_id)
    is_owner = (note.author_id == current_user_id)
    note_read = NoteRead(title=note.title, content=note.content, author_login=author_login, is_owner=is_owner)
    return note_read
