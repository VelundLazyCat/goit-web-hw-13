from fastapi import APIRouter, Depends, status, UploadFile, File, BackgroundTasks, HTTPException, Request
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from my_db import get_db
from models import User
import users as repository_users
from auth import auth_service
from config import settings
from shemas import UserDb
from email import send_email_password


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    cloudinary.uploader.upload(
        file.file, public_id=f'ContactsApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'ContactsApp/{current_user.username}') \
        .build_url(width=250, height=250, crop='fill')
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user


@router.patch('/update_password', response_model=UserDb)
async def update_password_user(password, background_tasks: BackgroundTasks, request: Request, current_user: User = Depends(auth_service.get_current_user),
                               db: Session = Depends(get_db)):
    password = auth_service.get_password_hash(password)
    user = await repository_users.update_user_password(current_user.email, password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    background_tasks.add_task(
        send_email_password, user.email, user.username, request.base_url)
    return user
