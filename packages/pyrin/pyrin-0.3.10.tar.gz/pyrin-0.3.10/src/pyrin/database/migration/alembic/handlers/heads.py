# -*- coding: utf-8 -*-
"""
database migration alembic handlers heads module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.base import AlembicReportingCLIHandlerBase
from pyrin.database.migration.alembic.handlers.params import ResolveDependenciesParamMixin


@alembic_cli_handler()
class HeadsCLIHandler(AlembicReportingCLIHandlerBase, ResolveDependenciesParamMixin):
    """
    heads cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of HeadsCLIHandler.
        """

        super().__init__('heads')
