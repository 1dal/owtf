"""
owtf.db.command_register
~~~~~~~~~~~~~~~~~~~~~~~~

Component to handle data storage and search of all commands run
"""

from sqlalchemy.exc import SQLAlchemyError

from owtf.dependency_management.dependency_resolver import BaseComponent
from owtf.dependency_management.interfaces import CommandRegisterInterface

from owtf.database import db
from owtf.command_register.models import Command
from owtf.target.service import target_required


def add_command(command):
    """Adds a command to the DB

    :param command: Command to add
    :type command: `dict`
    :return: None
    :rtype: None
    """
    db.session.merge(Command(
        start_time=command['Start'],
        end_time=command['End'],
        success=command['Success'],
        target_id=command['Target'],
        plugin_key=command['PluginKey'],
        modified_command=command['ModifiedCommand'].strip(),
        original_command=command['OriginalCommand'].strip()
    ))
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

def del_command(command):
    """Delete the command from the DB

    :param command: Command to delete
    :type command: `dict`
    :return: None
    :rtype: None
    """
    command_obj = db.session.query(Command).get(command)
    db.session.delete(command_obj)
    db.session.commit()

@target_required
def command_already_registered(original_command, target_id=None):
    """Checks if the command has already been registered

    :param original_command: Original command to check
    :type original_command: `dict`
    :param target_id: Target ID
    :type target_id: `int`
    :return: None
    :rtype: None
    """
    register_entry = db.session.query(Command).get(original_command)
    if register_entry:
        # If the command was completed and the plugin output to which it
        # is referring exists
        if register_entry.success:
            if plugin_output.plugin_output_exists(register_entry.plugin_key, register_entry.target_id):
                return target.get_target_url_for_id(register_entry.target_id)
            else:
                del_command(original_command)
                return None
        else:  # Command failed
            del_command(original_command)
            return target.get_target_url_for_id(register_entry.target_id)
    return None
