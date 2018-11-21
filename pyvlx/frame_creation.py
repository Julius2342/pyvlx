"""Helper module for creating a frame out of raw data."""
from .frame_get_scene_list import FrameGetSceneListRequest, FrameGetSceneListConfirmation, FrameGetSceneListNotification
from .frame_get_node_information import FrameGetNodeInformationRequest, FrameGetNodeInformationConfirmation, FrameGetNodeInformationNotification
from .frame_get_all_nodes_information import FrameGetAllNodesInformationRequest, FrameGetAllNodesInformationConfirmation, \
    FrameGetAllNodesInformationNotification, FrameGetAllNodesInformationFinishedNotification
from .frame_password_enter import FramePasswordEnterRequest, FramePasswordEnterConfirmation
from .frame_discover_nodes import FrameDiscoverNodesRequest, FrameDiscoverNodesConfirmation, FrameDiscoverNodesNotification
from .frame_error_notification import FrameErrorNotification
from .frame_command_send import FrameCommandSendRequest, FrameCommandSendConfirmation, FrameCommandRunStatusNotification, \
    FrameCommandRemainingTimeNotification, FrameSessionFinishedNotification
from .frame_activate_scene import FrameActivateSceneRequest, FrameActivateSceneConfirmation
from .const import Command
from .frame_helper import extract_from_frame


def frame_from_raw(raw):
    """Create and return frame from raw bytes."""
    command, payload = extract_from_frame(raw)
    frame = create_frame(command)
    if frame is None:
        print("Command {0} not implemented, raw: {1}".format(command, ":".join("{:02x}".format(c) for c in raw)))
        return None
    frame.from_payload(payload)
    return frame


def create_frame(command):
    """Create and return empty Frame from Command."""
    # pylint: disable=too-many-branches,too-many-return-statements
    if command == Command.GW_ERROR_NTF:
        return FrameErrorNotification()
    if command == Command.GW_COMMAND_SEND_REQ:
        return FrameCommandSendRequest()
    if command == Command.GW_COMMAND_SEND_CFM:
        return FrameCommandSendConfirmation()
    if command == Command.GW_COMMAND_RUN_STATUS_NTF:
        return FrameCommandRunStatusNotification()
    if command == Command.GW_COMMAND_REMAINING_TIME_NTF:
        return FrameCommandRemainingTimeNotification()
    if command == Command.GW_SESSION_FINISHED_NTF:
        return FrameSessionFinishedNotification()

    if command == Command.GW_PASSWORD_ENTER_REQ:
        return FramePasswordEnterRequest()
    if command == Command.GW_PASSWORD_ENTER_CFM:
        return FramePasswordEnterConfirmation()

    if command == Command.GW_CS_DISCOVER_NODES_REQ:
        return FrameDiscoverNodesRequest()
    if command == Command.GW_CS_DISCOVER_NODES_CFM:
        return FrameDiscoverNodesConfirmation()
    if command == Command.GW_CS_DISCOVER_NODES_NTF:
        return FrameDiscoverNodesNotification()

    if command == Command.GW_GET_SCENE_LIST_REQ:
        return FrameGetSceneListRequest()
    if command == Command.GW_GET_SCENE_LIST_CFM:
        return FrameGetSceneListConfirmation()
    if command == Command.GW_GET_SCENE_LIST_NTF:
        return FrameGetSceneListNotification()

    if command == Command.GW_GET_NODE_INFORMATION_REQ:
        return FrameGetNodeInformationRequest()
    if command == Command.GW_GET_NODE_INFORMATION_CFM:
        return FrameGetNodeInformationConfirmation()
    if command == Command.GW_GET_NODE_INFORMATION_NTF:
        return FrameGetNodeInformationNotification()

    if command == Command.GW_GET_ALL_NODES_INFORMATION_REQ:
        return FrameGetAllNodesInformationRequest()
    if command == Command.GW_GET_ALL_NODES_INFORMATION_CFM:
        return FrameGetAllNodesInformationConfirmation()
    if command == Command.GW_GET_ALL_NODES_INFORMATION_NTF:
        return FrameGetAllNodesInformationNotification()
    if command == Command.GW_GET_ALL_NODES_INFORMATION_FINISHED_NTF:
        return FrameGetAllNodesInformationFinishedNotification()

    if command == Command.GW_ACTIVATE_SCENE_REQ:
        return FrameActivateSceneRequest()
    if command == Command.GW_ACTIVATE_SCENE_CFM:
        return FrameActivateSceneConfirmation()
    return None
