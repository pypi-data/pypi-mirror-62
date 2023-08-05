from .base import MWRAPBase
from ..const import API_PATH

class Unit(MWRAPBase):
    """Class for handling units/teams."""

    def __init__(self, moco):
        self._moco = moco


    def get(
        self,
        id: int
        ):
        """Get a single team

        :param id: id of the team
        :returns: team object
        """

        return self._moco.get(API_PATH["unit_get"].format(id=id))

    def getlist(
        self,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """Get a list of teams
        
        :param sort_by: Sort by field
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of team objects
        """

        params = {}

        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["unit_getlist"], params=params)



    