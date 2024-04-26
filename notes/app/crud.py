from sqlalchemy import select, desc
from sqlalchemy.future import select

from database import Note


async def sql_query(author_id, from_date_obj, limit, offset, to_date_obj):
    query = select(Note)
    query = await author_handler(author_id, query)
    query = await from_data_handler(from_date_obj, query)
    query = await to_data_handler(query, to_date_obj)
    query = query.order_by(desc(Note.creation_date)).limit(offset).offset((limit - 1) * offset)
    return query


async def author_handler(author_id, query):
    if author_id:
        query = query.where(Note.author_id == author_id)
    return query


async def to_data_handler(query, to_date_obj):
    if to_date_obj:
        query = query.where(Note.creation_date <= to_date_obj)
    return query


async def from_data_handler(from_date_obj, query):
    if from_date_obj:
        query = query.where(Note.creation_date >= from_date_obj)
    return query
