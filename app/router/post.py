from typing import List, Optional
from fastapi import Response, status, HTTPException, Request, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=["Post"]
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user), 
              limit:int = 10, skip:int = 0,
              search:Optional[str]=""):
    # all_posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).limit(limit=limit).offset(offset=offset).all()
    # all_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
    
    print(result)
    return sorted(result, key=lambda x : x.votes, reverse=True)
    # return all_posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db), 
                 current_user:models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter_by(id=id).one_or_none()
    post = db.query(models.Post, func.count(models.Vote.post_id).label(
        "votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
        # models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post
    # return {"post_detail": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to Perform request action")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, update_post:schemas.PostCreate, db: Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to Perform request action")
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
