from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from ..database import get_db
from ..schemas import PatchNote, PatchNoteCreate, PatchNoteRead, PatchNoteUpdate
from ..errors import DataBaseError, PatchNoteError
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/patchnotes", tags=["patchnotes"])

@router.post("/", response_model=PatchNoteRead)
async def create_patchnote(patchnote: PatchNoteCreate, session: AsyncSession = Depends(get_db)):
    
    db_patchnote = PatchNote.model_validate(patchnote)
    logger.info(f"Creating patchnote : {db_patchnote}")
    session.add(db_patchnote)
    try:
        await session.commit()
        await session.refresh(db_patchnote)
    except SQLAlchemyError as sql_error:
        try:
            logger.error(f"{DataBaseError.CONNECTION_ERROR.value} : {sql_error}. Attempting rollback.")
            await session.rollback()
        except SQLAlchemyError as rollback_error:
            logger.error(f"{DataBaseError.ROLLBACK_ERROR.value} : {rollback_error}.")
            raise HTTPException(status_code=500, detail={"code": DataBaseError.ROLLBACK_ERROR.value}) from rollback_error
        logger.info(f"Rollback successful.")
        raise HTTPException(status_code=500, detail={"code":DataBaseError.CONNECTION_ERROR.value}) from sql_error
    logger.info(f"Patchnote successfully added.")
    return db_patchnote

@router.get("/get_all", response_model=list[PatchNoteRead])
async def get_all_patchnotes(session: AsyncSession = Depends(get_db)):
    logger.info("Getting patchnote list...")
    statement = select(PatchNote).order_by(desc(PatchNote.published_at))
    try:
        results = await session.execute(statement=statement)
    except SQLAlchemyError as sql_error:
        logger.error(f"{DataBaseError.CONNECTION_ERROR.value} : {sql_error}.")
        raise HTTPException(status_code=500, detail={"code":DataBaseError.CONNECTION_ERROR.value}) from sql_error
    results = results.scalars().all()
    logger.info(f"Patchnote list : {results}")
    return results

@router.patch("/update/{id}", response_model=PatchNoteRead)
async def update_patchnote(id: uuid.UUID, patchnote_update_data: PatchNoteUpdate , session: AsyncSession = Depends(get_db)):
    patchnote_update_dict = patchnote_update_data.model_dump(exclude_unset=True)
    logger.info(f"Updating patchnote {id} with new values : {patchnote_update_dict}")
    statement = select(PatchNote).where(PatchNote.id == id)
    try:
        results = await session.execute(statement=statement)
    except SQLAlchemyError as sql_error:
        logger.error(f"{DataBaseError.CONNECTION_ERROR.value} : {sql_error}.")
        raise HTTPException(status_code=500, detail={"code":DataBaseError.CONNECTION_ERROR.value}) from sql_error
    db_patchnote = results.scalars().one_or_none()
    if db_patchnote is None:
        logger.warning(f"{PatchNoteError.MISSING_ERROR.value} : patchnote {id} does not exists.")
        raise HTTPException(status_code=404, detail={"code":PatchNoteError.MISSING_ERROR.value, "id":id})
    logger.info(f"Patchnote {id} found ! Applying update.")
    db_patchnote.sqlmodel_update(patchnote_update_dict)
    try:
        await session.commit()
        await session.refresh(db_patchnote)
    except SQLAlchemyError as sql_error:
        logger.error(f"{DataBaseError.CONNECTION_ERROR.value} : {sql_error}. Attempting rollback.")
        try:
            await session.rollback()
            logger.info("Rollback successful.")
        except SQLAlchemyError as rollback_error:
            logger.error(f"{DataBaseError.ROLLBACK_ERROR.value} : {rollback_error}")
            raise HTTPException(status_code=500, detail={"code":DataBaseError.ROLLBACK_ERROR.value}) from rollback_error
        raise HTTPException(status_code=500, detail={"code":DataBaseError.CONNECTION_ERROR.value}) from sql_error
    logger.info(f"Patchnote {id} updated successfuly. New value : {db_patchnote}")
    return db_patchnote

@router.delete("/delete/{id}", status_code=204)
async def delete_patchnote(id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    logger.info(f"Attempting to delete patchnote {id}.")
    statement = select(PatchNote).where(PatchNote.id == id)
    try:
        results = await session.execute(statement=statement)
    except SQLAlchemyError as sql_error:
        logger.error(f"{DataBaseError.CONNECTION_ERROR.value} : {sql_error}.")
        raise HTTPException(status_code=500, detail={"code":DataBaseError.CONNECTION_ERROR.value}) from sql_error
    results = results.scalars().one_or_none()

    if results is None:
        logger.warning(f"{PatchNoteError.MISSING_ERROR.value} : patchnote {id} does not exists.")
        raise HTTPException(status_code=404, detail={"code":PatchNoteError.MISSING_ERROR.value, "id":id})
    logger.info(f"Patchnote {id} found ! Deleting.")

    try:
        await session.delete(results)
        await session.commit()
    except SQLAlchemyError as sql_error:
        logger.error(f"{DataBaseError.CONNECTION_ERROR.value} : {sql_error}.")
        try:
            logger.info("Attempting rollback...")
            await session.rollback()
        except SQLAlchemyError as rollback_error:
            logger.error(f"{DataBaseError.ROLLBACK_ERROR.value} : {rollback_error}.")
            raise HTTPException(status_code=500, detail={"code":DataBaseError.ROLLBACK_ERROR.value}) from rollback_error
        logger.info("Rollback successful.")
        raise HTTPException(status_code=500, detail={"code":DataBaseError.CONNECTION_ERROR.value}) from sql_error
    logger.info(f"Patchnote {id} successfully deleted.")