# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ExportBillsClassPermission(Model):
    """ExportBillsClassPermission.

    :param edit:
    :type edit: bool
    :param delete:
    :type delete: bool
    :param run:
    :type run: bool
    """

    _attribute_map = {
        'edit': {'key': 'edit', 'type': 'bool'},
        'delete': {'key': 'delete', 'type': 'bool'},
        'run': {'key': 'run', 'type': 'bool'},
    }

    def __init__(self, edit=None, delete=None, run=None):
        super(ExportBillsClassPermission, self).__init__()
        self.edit = edit
        self.delete = delete
        self.run = run
