from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/likes",
    tags=["likes"]
)

@router.post("/", status_code=status.HTTP_200_OK)
def toggle_like(
    action: schemas.LikeAction,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):


    """
    - action.liked == True  → add a like
    - action.liked == False → remove a like
    """

    # 1) Verify the target post exists
    post = db.query(models.Post).filter(models.Post.post_id == action.post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {action.post_id} not found."
        )

    # 2) Check if this user already has a like on that post
    like_query = db.query(models.Likes).filter(
        models.Likes.post_id == action.post_id,
        models.Likes.user_id == current_user.user_id        # type: ignore
    )
    existing = like_query.first()

    if action.liked:
        # Client wants to add a like
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You’ve already liked this post."
            )
        new_like = models.Likes(
            post_id=action.post_id,
            user_id=current_user.user_id        # type: ignore
        )
        db.add(new_like)
        db.commit()
        return {"message": "Post liked."}
    else:
        # Client wants to remove the like
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cannot remove like—none exists."
            )
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Like removed."}