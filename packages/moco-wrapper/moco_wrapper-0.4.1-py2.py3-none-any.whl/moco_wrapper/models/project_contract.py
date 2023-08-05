from .base import MWRAPBase
from ..const import API_PATH

class ProjectContract(MWRAPBase):
    """Class for handling project contracts."""

    def __init__(self, moco):
        self._moco = moco

    def create(
        self,
        project_id: int,
        user_id: int,
        billable: bool = None,
        active: bool = None,
        budget: float = None,
        hourly_rate: float = None
        ):
        """Assign a person to a project

        :param project: id of the project
        :param user_id: user id of the person to assign
        :param billable: true/false if the contract is billable
        :param active: true/false if the contract is active
        :param budget: contract budget
        :param hourly_rate: contract hourly rate
        :returns: create contract object
        """
        data = {
            "user_id": user_id
        }

        for key, value in (
            ("billable", billable),
            ("active", active),
            ("budget", budget),
            ("hourly_rate", hourly_rate)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["project_contract_create"].format(project_id=project_id), data=data)

    def update(
        self,
        project_id: int,
        contract_id: int,
        billable: bool= None,
        active: bool = None,
        budget: float = None,
        hourly_rate: float = None
        ):
        """update an existing staff assignment

        :param project_id: id of the project to update the contract for
        :param contract_id: id of the contract to update
        :param billable: true/false if the contract is billable
        :param active: true/false if the contract is active
        :param budget: contract budget
        :param hourly_rate: contract hourly rate
        :returns: the updated project contract
        """

        data = {}
        for key,value in (
            ("billable", billable),
            ("active", active),
            ("budget", budget),
            ("hourly_rate", hourly_rate)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["project_contract_update"].format(project_id=project_id, contract_id=contract_id), data=data)

    def get(
        self,
        project_id: int,
        contract_id: int
        ):
        """retrieve a single staff assignment of a project

        :param project_id: id of the project
        :param contract_id: id of the contract
        :returns: the contract object
        """

        return self._moco.get(API_PATH["project_contract_get"].format(project_id=project_id, contract_id=contract_id))

    def getlist(
        self,
        project_id: int,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """retrive all active staff assignments for a project

        :param project_id: id of the project
        :param sort_by: sort by field
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: a list of contract objects
        """

        params = {}

        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_contract_getlist"].format(project_id=project_id), params=params)

    def delete(
        self,
        project_id: int,
        contract_id: int,
        ):
        """delete a staff assignment

        deleting a staff assignment is only possible as long as no hours are tracked from this person

        :param project_id: id of the project
        :param contract_id: id of the contract to delete
        """

        return self._moco.delete(API_PATH["project_contract_delete"].format(project_id=project_id, contract_id=contract_id))




