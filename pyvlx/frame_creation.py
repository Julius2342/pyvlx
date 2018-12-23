"""Helper module for creating a frame out of raw data."""
from pyvlx.frames import (
    FrameActivateSceneConfirmation, FrameActivateSceneRequest,
    FrameActivationLogUpdatedNotification,
    FrameCommandRemainingTimeNotification, FrameCommandRunStatusNotification,
    FrameCommandSendConfirmation, FrameCommandSendRequest,
    FrameDiscoverNodesConfirmation, FrameDiscoverNodesNotification,
    FrameDiscoverNodesRequest, FrameErrorNotification,
    FrameGetAllNodesInformationConfirmation,
    FrameGetAllNodesInformationFinishedNotification,
    FrameGetAllNodesInformationNotification,
    FrameGetAllNodesInformationRequest, FrameGetNodeInformationConfirmation,
    FrameGetNodeInformationNotification, FrameGetNodeInformationRequest,
    FrameGetProtocolVersionConfirmation, FrameGetProtocolVersionRequest,
    FrameGetSceneListConfirmation, FrameGetSceneListNotification,
    FrameGetSceneListRequest, FrameGetStateConfirmation, FrameGetStateRequest,
    FrameGetVersionConfirmation, FrameGetVersionRequest,
    FrameHouseStatusMonitorDisableConfirmation,
    FrameHouseStatusMonitorDisableRequest,
    FrameHouseStatusMonitorEnableConfirmation,
    FrameHouseStatusMonitorEnableRequest,
    FrameNodeInformationChangedNotification,
    FrameNodeStatePositionChangedNotification, FramePasswordEnterConfirmation,
    FramePasswordEnterRequest, FrameSessionFinishedNotification,
    FrameSetNodeNameConfirmation, FrameSetNodeNameRequest,
    FrameSetUTCConfirmation, FrameSetUTCRequest, extract_from_frame)

from .const import Command
from .log import PYVLXLOG


def frame_from_raw(raw):
    """Create and return frame from raw bytes."""
    command, payload = extract_from_frame(raw)
    frame = create_frame(command)
    if frame is None:
        PYVLXLOG.warning("Command %s not implemented, raw: %s", command, ":".join("{:02x}".format(c) for c in raw))
        return None
    frame.validate_payload_len(payload)
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

    if command == Command.GW_GET_VERSION_REQ:
        return FrameGetVersionRequest()
    if command == Command.GW_GET_VERSION_CFM:
        return FrameGetVersionConfirmation()
    if command == Command.GW_GET_PROTOCOL_VERSION_REQ:
        return FrameGetProtocolVersionRequest()
    if command == Command.GW_GET_PROTOCOL_VERSION_CFM:
        return FrameGetProtocolVersionConfirmation()

    if command == Command.GW_SET_NODE_NAME_REQ:
        return FrameSetNodeNameRequest()
    if command == Command.GW_SET_NODE_NAME_CFM:
        return FrameSetNodeNameConfirmation()

    if command == Command.GW_NODE_INFORMATION_CHANGED_NTF:
        return FrameNodeInformationChangedNotification()

    if command == Command.GW_GET_STATE_REQ:
        return FrameGetStateRequest()
    if command == Command.GW_GET_STATE_CFM:
        return FrameGetStateConfirmation()

    if command == Command.GW_SET_UTC_REQ:
        return FrameSetUTCRequest()
    if command == Command.GW_SET_UTC_CFM:
        return FrameSetUTCConfirmation()

    if command == Command.GW_ACTIVATION_LOG_UPDATED_NTF:
        return FrameActivationLogUpdatedNotification()

    if command == Command.GW_HOUSE_STATUS_MONITOR_ENABLE_REQ:
        return FrameHouseStatusMonitorEnableRequest()
    if command == Command.GW_HOUSE_STATUS_MONITOR_ENABLE_CFM:
        return FrameHouseStatusMonitorEnableConfirmation()
    if command == Command.GW_HOUSE_STATUS_MONITOR_DISABLE_REQ:
        return FrameHouseStatusMonitorDisableRequest()
    if command == Command.GW_HOUSE_STATUS_MONITOR_DISABLE_CFM:
        return FrameHouseStatusMonitorDisableConfirmation()

    if command == Command.GW_NODE_STATE_POSITION_CHANGED_NTF:
        return FrameNodeStatePositionChangedNotification()

    return None
