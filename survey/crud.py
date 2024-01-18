from fastapi import FastAPI, HTTPException, Depends
from .models import *
import os


class Survey:
    
    async def add_user(user_data,response,db):
        try:
            # Extract user information
            email = user_data.get('email')
            name = user_data.get('name')
            language_id = user_data.get('language_id')

            # Check if the user with the given email already exists
            existing_user = db.query(Users).filter(Users.email == email).first()
            if existing_user:
                raise HTTPException(status_code=400, detail='User with this email already exists')

            # Check if the language_id exists
            language = db.query(Language).filter(Language.id == language_id).first()
            if not language:
                raise HTTPException(status_code=400, detail='Invalid language_id')

            # Create a new user
            new_user = Users(email=email, name=name, language_id=language_id)

            # Add the user to the database
            db.add(new_user)
            db.commit()

            return {'success': True,'data': 'User added successfully'}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def list_languages(db):
        languages = db.query(Language).all()

        return {'success': True,'data': languages}