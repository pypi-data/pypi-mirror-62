from .base import MWRAPBase
from ..const import API_PATH

from enum import Enum

class CommentTargetType(str, Enum):
    """
    Enumeration of types that a comment can be created for.

    If you comment on an Offer use CommentTargetType.OFFER and supply the offer id in the parameter commentable_id
    """
    USER = "User"
    DEAL = "Deal"
    OFFER = "Offer"
    OFFERCONFIRMATION = "OfferConfirmation"
    CUSTOMER = "Customer"
    PROJECT = "Project"
    INVOICE = "Invoice"
    CONTACT = "Contact"

class Comment(MWRAPBase):
    """Class for handling comments."""

    def __init__(self, moco):
        self._moco = moco

    def create(
        self,
        commentable_id: int,
        commentable_type: CommentTargetType,
        text: str
        ):
        """create a comment 

        :param commentable_id: id of the object to create the comment of (i.e the project id of the project we want to comment on)
        :param commentable_type: type of object to create the comment of (i.e when we want to comment on a project this is "project"), available values are  "User", "Deal", "Offer", "OfferConfirmation", "Customer", "Project", "Invoice", "Contact"
        :param text: comment text
        :returns: the created comment
        """
        data = {
            "commentable_id": commentable_id,
            "commentable_type" : commentable_type,
            "text": text
        }

        return self._moco.post(API_PATH["comment_create"], data=data)

    def create_bulk(
        self,
        commentable_ids: list,
        commentable_type: CommentTargetType,
        text: str
        ):
        """create a comment under multplie objects of the same type
        :param commentable_ids: ids of the objects we want to comment under ie. [123, 124, 125]
        :param commentable_type: type of object to create the comment of (i.e when we want to comment on a project this is "project"), available values are  "User", "Deal", "Offer", "OfferConfirmation", "Customer", "Project", "Invoice", "Contact"
        :param text: comment text
        """
        data = {
            "commentable_ids" : commentable_ids,
            "commentable_type": commentable_type,
            "text" : text
        }

        return self._moco.post(API_PATH["comment_create_bulk"], data=data)

    def update(
        self,
        id: int,
        text: str
        ):
        """update a comment

        :param id: the id of the comment to update
        :param text: comment text
        :returns: the created comment
        """
        data = {
            "text" : text,  
        }

        return self._moco.put(API_PATH["comment_update"].format(id=id), data=data)

    def delete(
        self,
        id: int,
        ):
        """delete a comment

        :param id: id of the comment to delete
        """

        return self._moco.delete(API_PATH["comment_delete"].format(id=id))

    def get(
        self,
        id: int
        ):
        """retrieve a single comment

        :param id: id of the comment
        :returns: a single comment object
        """
        return self._moco.get(API_PATH["comment_get"].format(id=id))

    def getlist(
        self,
        commentable_type: CommentTargetType = None,
        commentable_id: int = None,
        user_id: int = None,
        manual: bool = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """retrieve a list of comments

        :param commentable_type: type of object the comment(s) belong to available values are  "User", "Deal", "Offer", "OfferConfirmation", "Customer", "Project", "Invoice", "Contact"
        :param commentable_id: id of the object the comment belongs to
        :param user_id: user id of the creator
        :param manual: true/false user-created of generated
        :param sort_by: field to sort the results by
        :param sort_order: asc or desc
        :param page: page number (default 1)
        :returns: list of comemnt objects
        """
        params = {}
        for key, value in (
            ("commentable_type", commentable_type),
            ("commentable_id", commentable_id),
            ("user_id", user_id),
            ("manual", manual),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["comment_getlist"], params=params)


        