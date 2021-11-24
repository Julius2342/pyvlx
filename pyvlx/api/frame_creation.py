"""Helper module for creating a frame out of raw data."""
from pyvlx.const import Command
from pyvlx.log import PYVLXLOG

from .frames import (
    FrameActivateSceneConfirmation, FrameActivateSceneRequest,
    FrameActivationLogUpdatedNotification,
    FrameCommandRemainingTimeNotification, FrameCommandRunStatusNotification,
    FrameCommandSendConfirmation, FrameCommandSendRequest,
    FrameDiscoverNodesConfirmation, FrameDiscoverNodesNotification,
    FrameDiscoverNodesRequest, FrameErrorNotification,
    FrameGatewayFactoryDefaultConfirmation, FrameGatewayFactoryDefaultRequest,
    FrameGatewayRebootConfirmation, FrameGatewayRebootRequest,
    FrameGetAllNodesInformationConfirmation,
    FrameGetAllNodesInformationFinishedNotification,
    FrameGetAllNodesInformationNotification,
    FrameGetAllNodesInformationRequest, FrameGetLimitationStatus,
    FrameGetLimitationStatusConfirmation, FrameGetLimitationStatusNotification,
    FrameGetLocalTimeConfirmation, FrameGetLocalTimeRequest,
    FrameGetNetworkSetupConfirmation, FrameGetNetworkSetupRequest,
    FrameGetNodeInformationConfirmation, FrameGetNodeInformationNotification,
    FrameGetNodeInformationRequest, FrameGetProtocolVersionConfirmation,
    FrameGetProtocolVersionRequest, FrameGetSceneListConfirmation,
    FrameGetSceneListNotification, FrameGetSceneListRequest,
    FrameGetStateConfirmation, FrameGetStateRequest,
    FrameGetVersionConfirmation, FrameGetVersionRequest,
    FrameHouseStatusMonitorDisableConfirmation,
    FrameHouseStatusMonitorDisableRequest,
    FrameHouseStatusMonitorEnableConfirmation,
    FrameHouseStatusMonitorEnableRequest, FrameLeaveLearnStateConfirmation,
    FrameLeaveLearnStateRequest, FrameNodeInformationChangedNotification,
    FrameNodeStatePositionChangedNotification, FramePasswordChangeConfirmation,
    FramePasswordChangeNotification, FramePasswordChangeRequest,
    FramePasswordEnterConfirmation, FramePasswordEnterRequest,
    FrameSessionFinishedNotification, FrameSetNodeNameConfirmation,
    FrameSetNodeNameRequest, FrameSetUTCConfirmation, FrameSetUTCRequest,
    FrameStatusRequestConfirmation, FrameStatusRequestNotification,
    FrameStatusRequestRequest, extract_from_frame)


def frame_from_raw(raw):
    """Create and return frame from raw bytes."""
    command, payload = extract_from_frame(raw)
    frame = create_frame(command)
    if frame is None:
        PYVLXLOG.warning(
            "Command %s not implemented, raw: %s",
            command,
            ":".join("{:02x}".format(c) for c in raw),
        )
        return None
    frame.validate_payload_len(payload)
    frame.from_payload(payload)
    return frame


def create_frame(command):
    """Create and return empty Frame from Command."""
    # pylint: disable=too-many-branches,too-many-return-statements,too-many-statements
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

    if command == Command.GW_PASSWORD_CHANGE_REQ:
        return FramePasswordChangeRequest()
    if command == Command.GW_PASSWORD_CHANGE_CFM:
        return FramePasswordChangeConfirmation()
    if command == Command.GW_PASSWORD_CHANGE_NTF:
        return FramePasswordChangeNotification()

    if command == Command.GW_REBOOT_REQ:
        return FrameGatewayRebootRequest()
    if command == Command.GW_REBOOT_CFM:
        return FrameGatewayRebootConfirmation()

    if command == Command.GW_SET_FACTORY_DEFAULT_REQ:
        return FrameGatewayFactoryDefaultRequest()
    if command == Command.GW_SET_FACTORY_DEFAULT_CFM:
        return FrameGatewayFactoryDefaultConfirmation()

    if command == Command.GW_GET_LOCAL_TIME_REQ:
        return FrameGetLocalTimeRequest()
    if command == Command.GW_GET_LOCAL_TIME_CFM:
        return FrameGetLocalTimeConfirmation()

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

    if command == Command.GW_GET_LIMITATION_STATUS_REQ:
        return FrameGetLimitationStatus()
    if command == Command.GW_GET_LIMITATION_STATUS_CFM:
        return FrameGetLimitationStatusConfirmation()
    if command == Command.GW_LIMITATION_STATUS_NTF:
        return FrameGetLimitationStatusNotification()

    if command == Command.GW_GET_NETWORK_SETUP_REQ:
        return FrameGetNetworkSetupRequest()
    if command == Command.GW_GET_NETWORK_SETUP_CFM:
        return FrameGetNetworkSetupConfirmation()

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
    if command == Command.GW_LEAVE_LEARN_STATE_CFM:
        return FrameLeaveLearnStateConfirmation()
    if command == Command.GW_LEAVE_LEARN_STATE_REQ:
        return FrameLeaveLearnStateRequest()

    if command == Command.GW_STATUS_REQUEST_REQ:
        return FrameStatusRequestRequest()
    if command == Command.GW_STATUS_REQUEST_CFM:
        return FrameStatusRequestConfirmation()
    if command == Command.GW_STATUS_REQUEST_NTF:
        return FrameStatusRequestNotification()

    return None
