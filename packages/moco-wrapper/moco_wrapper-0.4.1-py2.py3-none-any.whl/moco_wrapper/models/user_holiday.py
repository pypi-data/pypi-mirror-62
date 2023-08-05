from .base import MWRAPBase
from ..const import API_PATH

class UserHoliday(MWRAPBase):
    """class for handling holidays (in german urlaubsanspruch)."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        year: int = None,
        user_id: int = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """retrieve a list of holidays

        :param year: show only this year (ex. 2019)
        :param user_id: show only holidays from this user (ex. 5)
        :param sort_by: field to sort results by
        :param sort_order: asc or desc
        :param page: page number (default 1)
        :returns: asc or desc
        """
        params = {}
        for key, value in (
            ("year", year),
            ("user_id", user_id),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order) 

        return self._moco.get(API_PATH["holiday_getlist"], params=params)
    
    def get(
        self,
        id: int
        ):
        """retrieve single holiday

        :param id: id of the holiday
        :returns: the holiday object
        """
        return self._moco.get(API_PATH["holiday_get"].format(id=id))

    def create(
        self,
        year: int, 
        title: str,
        user_id: int,
        hours: int = 0
        ):
        """create an users entitilement for holidays

        :param year: year of the holiday (ex. 2019)
        :param title: title of the holiday
        :param user_id: user_id this holiday belongs to
        :param hours: hours (ex. 160) (default 0)
        :returns: the created holiday object
        """
        data = {
            "year" : year,
            "title": title,
            "hours": hours,
            "user_id": user_id,
        }

        return self._moco.post(API_PATH["holiday_create"], data=data)

    def update(
        self,
        id: int,
        year: int = None,
        title: str = None,
        user_id: int = None,
        hours: int = None,
        ):
        """update a holiday

        :param id: id of the holiday
        :param year: year of the holiday (ex. 2019)
        :param title: title of the holiday
        :param hours: hours (ex. 160)
        :param user_id: user_id this holiday belongs to
        :returns: the created holiday object
        """
        
        data = {}
        for key, value in (
            ("year", year),
            ("title", title),
            ("hours", hours),
            ("user_id", user_id)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["holiday_update"].format(id=id), data=data)

    def delete(
        self,
        id: int
        ):
        """delete a holiday

        :param id: id of the holiday to delete
        """
        return self._moco.delete(API_PATH["holiday_delete"].format(id=id))
