
from fastapi import APIRouter, HTTPException, Depends, status, Query
from my_db import get_db
from shemas import ContactSchema, ContactResponse
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter
import contacts
from contacts import User
from auth import auth_service


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=list[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts(contact_field: str = Query(None), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contacts_ = await contacts.get_contacts(contact_field, current_user, db)
    if contacts_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='CONTACTS NOT FOUND')
    return contacts_


@router.get('/{contact_id}', response_model=ContactResponse,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='CONTACT NOT FOUND')
    return contact


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactSchema, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await contacts.create_contact(body, current_user, db)
    return contact


@router.put('/{contact_id}', response_model=ContactResponse,
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactSchema, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='CONTACT NOT FOUND')
    return contact


@router.delete('/{contact_id}', response_model=ContactResponse,
               description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def delete_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await contacts.delete_contact(contact_id, current_user, db)
    return contact


@router.get('/7', response_model=list[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts_birthdays(db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    contacts_ = await contacts.get_contacts_birthdays(current_user, db)
    if contacts_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='CONTACTS NOT FOUND')
    return contacts_
