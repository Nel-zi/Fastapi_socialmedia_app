from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import or_, func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db

# # This removes the prefix "post" from all the path operators and also add tags on the swagger UI
# router = APIRouter(
#     prefix="/posts",
#     tags=['Post']
#     )



# # @router.get("/", response_model=List[schemas.Post])
# @router.get("/", response_model=List[schemas.PostOut])
# def get_posts(db: Session = Depends(get_db),  
#               #Adding a query parameters
#               limit: int=10, skip: int=0, search: Optional[str]=""):
    
#     posts = db.query(models.Post).filter(or_(models.Post.title.contains(search),
#                                              models.Post.content.contains(search))
#                                              ).limit(limit).offset(skip).all()
    
#     results = db.query(models.Post, func.count(models.Likes.post_id).label("likes")).join(
#         models.Likes, models.Likes.post_id == models.Post.post_id, isouter=True).group_by(models.Post.post_id).all()


#     # posts = db.query(models.Post, func.count(models.Likes.post_id).label("likes")).join(
#     #     models.Likes, models.Likes.post_id == models.Post.post_id, isouter=True).group_by(models.Post.post_id).filter(
#     #         models.Post.title.contains(search)).limit(limit).offset(skip).all()   

  
#     return results










router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    """
    Fetch a paginated list of posts, each with:
      - its own fields (title, content, published, created_at, user_id, user)
      - a computed 'likes' count
    """

    # Join Post ↔ Likes so we can count how many likes each post has
    rows = (
        db.query(
            models.Post,
            func.count(models.Likes.post_id).label("likes")
        )
        .join(
            models.Likes,
            models.Likes.post_id == models.Post.post_id,
            isouter=True
        )
        .group_by(models.Post.post_id)
        .filter(
            or_(
                models.Post.title.contains(search),
                models.Post.content.contains(search)
            )
        )
        .limit(limit)
        .offset(skip)
        .all()
    )

    results = []
    for post_obj, likes_count in rows:
        # Explicitly construct a dict matching PostOut
        results.append({
            "post_id":    post_obj.post_id,
            "title":      post_obj.title,
            "content":    post_obj.content,
            "published":  post_obj.published,
            "created_at": post_obj.created_at,
            "user_id":    post_obj.user_id,
            "user": {
                "user_id":    post_obj.user.user_id,
                "email":      post_obj.user.email,
                "created_at": post_obj.user.created_at
            },
            "likes": likes_count
        })

    return results








@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    #print(current_user.email)
    new_post = models.Post(user_id=current_user.user_id, **post.dict()) # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int,  db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.post_id==post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")
    return post



@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.post_id==post_id)

    post = post_query.first()
    

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")
    

    if post.user_id != current_user.user_id:                                # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.post_id==post_id)
    post= post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")
    

    if post.user_id != current_user.user_id:                       # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.update(dict(updated_post), synchronize_session=False)
    db.commit()

    #updated_post.dict()
    
    return post_query.first()