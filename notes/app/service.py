from dateutil.parser import isoparse
from fastapi import HTTPException

from crud import sql_query


async def get_notes(author_id, from_date_obj, limit, offset, session, to_date_obj):
    query = await sql_query(author_id, from_date_obj, limit, offset, to_date_obj)
    result = await session.execute(query)
    notes = result.scalars().all()
    return notes


async def get_data(from_date):
    return isoparse(from_date) if from_date else None


async def validate_date_parameters(from_date_obj, to_date_obj):
    if from_date_obj and to_date_obj and from_date_obj > to_date_obj:
        raise HTTPException(status_code=400,
                            detail="Invalid date range. 'from_date' must be earlier than 'to_date'.")
