from maya import cmds
from maya import OpenMaya


def sanitycheck():
    """Return True if all checks passed

    Returns:
        bool: All checks passed
    """
    to_check = (check_scene_status, check_selection)

    for check in to_check:
        if not check():
            return False

    return True


def _error_dialog(error_type):
    error_messages = {
        "one_or_multiple_selection": "Clear your selection before running Quickblast",
        "not_saved": "Save your file before running Quickblast.",
    }

    if OpenMaya.MGlobal.mayaState() == OpenMaya.MGlobal.kInteractive:
        cmds.confirmDialog(
            title="Error: Quickblast",
            message=error_messages[error_type],
            button=[
                "Ok",
            ],
        )

    else:
        OpenMaya.MGlobal.displayError(error_messages[error_type])

    return False


def check_selection():
    """Check if there is no selection

    Returns:
        bool: Check success
    """

    # Get selection
    selection = cmds.ls(sl=True)

    if selection:
        return _error_dialog("one_or_multiple_selection")

    return True


def check_scene_status():
    """Check if the scene is saved

    Returns:
        bool: Check success
    """
    if cmds.file(query=True, modified=True):
        return _error_dialog("not_saved")

    return True


def check_sound_node():
    """Check if there is a sound node

    Returns:
        bool: Check success
    """
    # Get sound node
    node = cmds.ls(type="audio")

    if not node:
        return False

    return True
