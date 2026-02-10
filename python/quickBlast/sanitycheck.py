from maya import cmds
from maya import OpenMaya


def sanitycheck(show_popup_errors: bool):
    """Return True if all checks passed.
    If show_popup_errors, display a confirm dialog.

    Returns:
        bool: All checks passed
    """
    to_check = (check_selection, check_time_slider)

    for check in to_check:
        if not check(show_popup_errors = show_popup_errors):
            return False

    return True


def _error_dialog(error_type, show_popup_errors = True):
    error_messages = {
        "one_or_multiple_selection": "Clear your selection before running Quickblast",
        "not_saved": "Save your file before running Quickblast.",
        "negative_frames": "Cannot quickblast negative frames.",
    }

    if OpenMaya.MGlobal.mayaState() == OpenMaya.MGlobal.kInteractive and show_popup_errors:
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


def check_selection(show_popup_errors):
    """Check if there is no selection

    Returns:
        bool: Check success
    """

    # Get selection
    selection = cmds.ls(sl=True)

    if selection:
        return _error_dialog("one_or_multiple_selection", show_popup_errors = show_popup_errors)

    return True


def check_scene_status(show_popup_errors):
    """Check if the scene is saved

    Returns:
        bool: Check success
    """
    if cmds.file(query=True, modified=True):
        return _error_dialog("not_saved", show_popup_errors = show_popup_errors)

    return True


def check_sound_node():
    """Check if there is a sound node

    Returns:
        bool: Check success
    """
    # Get sound node
    node = cmds.ls(type="audio")

    if len(node) > 1:
        OpenMaya.MGlobal.displayWarning(
            "Multiple audio nodes are detected. Your quickblast might not sound as expected."
        )

    if not node:
        return False

    return True


def check_time_slider(show_popup_errors):
    """Check if the time slider is in the positive range

    Returns:
        bool: Check success
    """
    # We have to make sure the time slider is in the positive range
    # to avoid a filename not found error
    # This happens when an expected format (%04d) gets f*cked
    # because of the minus (three digits '-001' instead of four digits)

    if cmds.playbackOptions(query=True, min=True) < 0:
        return _error_dialog("negative_frames", show_popup_errors = show_popup_errors)

    return True
