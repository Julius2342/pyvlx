"""Module for enum and consts."""

from enum import Enum


class Command(Enum):
    """Enum class for GW Command bytes."""

    # pylint: disable=invalid-name

    GW_ERROR_NTF = 0x0000
    GW_REBOOT_REQ = 0x0001
    GW_REBOOT_CFM = 0x0002

    GW_SET_FACTORY_DEFAULT_REQ = 0x0003
    GW_SET_FACTORY_DEFAULT_CFM = 0x0004

    GW_GET_VERSION_REQ = 0x0008
    GW_GET_VERSION_CFM = 0x0009

    GW_GET_PROTOCOL_VERSION_REQ = 0x000A
    GW_GET_PROTOCOL_VERSION_CFM = 0x000B

    GW_GET_STATE_REQ = 0x000C
    GW_GET_STATE_CFM = 0x000D

    GW_LEAVE_LEARN_STATE_REQ = 0x000E
    GW_LEAVE_LEARN_STATE_CFM = 0x000F

    GW_GET_NETWORK_SETUP_REQ = 0x00E0
    GW_GET_NETWORK_SETUP_CFM = 0x00E1
    GW_SET_NETWORK_SETUP_REQ = 0x00E2
    GW_SET_NETWORK_SETUP_CFM = 0x00E3

    GW_CS_GET_SYSTEMTABLE_DATQ_REQ = 0x0100
    GW_CS_GET_SYSTEMTABLE_DATA_CFM = 0x0101
    GW_CS_GET_SYSTEMTABLE_DATA_NTF = 0x0102

    GW_CS_DISCOVER_NODES_REQ = 0x0103
    GW_CS_DISCOVER_NODES_CFM = 0x0104
    GW_CS_DISCOVER_NODES_NTF = 0x0105

    GW_CS_REMOVE_NODES_REQ = 0x0106
    GW_CS_REMOVE_NODES_CFM = 0x0107

    GW_CS_VIRGIN_STATE_REQ = 0x0108
    GW_CS_VIRGIN_STATE_CFM = 0x0109

    GW_CS_CONTROLLER_COPY_REQ = 0x010A
    GW_CS_CONTROLLER_COPY_CFM = 0x010B
    GW_CS_CONTROLLER_COPY_NTF = 0x010C
    GW_CS_CONTROLLER_COPY_CANCEL_NTF = 0x010D

    GW_CS_RECEIVE_KEY_REQ = 0x010E
    GW_CS_RECEIVE_KEY_CFM = 0x010F
    GW_CS_RECEIVE_KEY_NTF = 0x0110

    GW_CS_PGC_JOB_NTF = 0x0111
    GW_CS_SYSTEM_TABLE_UPDATE_NTF = 0x0112
    GW_CS_GENERATE_NEW_KEY_REQ = 0x0113
    GW_CS_GENERATE_NEW_KEY_CFM = 0x0114
    GW_CS_GENERATE_NEW_KEY_NTF = 0x0115

    GW_CS_REPAIR_KEY_REQ = 0x0116
    GW_CS_REPAIR_KEY_CFM = 0x0117
    GW_CS_REPAID_KEY_NTF = 0x0118

    GW_CS_ACTIVATE_CONFIGURATION_MODE_REQ = 0x0119
    GW_CS_ACTIVATE_CONFIGURATION_MODE_CFM = 0x011A

    GW_GET_NODE_INFORMATION_REQ = 0x0200
    GW_GET_NODE_INFORMATION_CFM = 0x0201
    GW_GET_NODE_INFORMATION_NTF = 0x0210

    GW_GET_ALL_NODES_INFORMATION_REQ = 0x0202
    GW_GET_ALL_NODES_INFORMATION_CFM = 0x0203
    GW_GET_ALL_NODES_INFORMATION_NTF = 0x0204
    GW_GET_ALL_NODES_INFORMATION_FINISHED_NTF = 0x0205

    GW_SET_NODE_VARIATION_REQ = 0x0206
    GW_SET_NODE_VARIATION_CFM = 0x0207

    GW_SET_NODE_NAME_REQ = 0x0208
    GW_SET_NODE_NAME_CFM = 0x0209

    GW_SET_NODE_VELOCITY_REQ = 0x020A
    GW_SET_NODE_VELOCITY_CFM = 0x020B

    GW_NODE_INFORMATION_CHANGED_NTF = 0x020C

    GW_NODE_STATE_POSITION_CHANGED_NTF = 0x0211

    GW_SET_NODE_ORDER_AND_PLACEMENT_REQ = 0x020D
    GW_SET_NODE_ORDER_AND_PLACEMENT_CFM = 0x020E

    GW_GET_GROUP_INFORMATION_REQ = 0x0220
    GW_GET_GROUP_INFORMATION_CFM = 0x0221
    GW_GET_GROUP_INFORMATION_NTF = 0x0230

    GW_SET_GROUP_INFORMATION_REQ = 0x0222
    GW_SET_GROUP_INFORMATION_CFM = 0x0223

    GW_GROUP_INFORMATION_CHANGED_NTF = 0x0224

    GW_DELETE_GROUP_REQ = 0x0225
    GW_DELETE_GROUP_CFM = 0x0226

    GW_NEW_GROUP_REQ = 0x0227
    GW_NEW_GROUP_CFM = 0x0228

    GW_GET_ALL_GROUPS_INFORMATION_REQ = 0x0229
    GW_GET_ALL_GROUPS_INFORMATION_CFM = 0x022A
    GW_GET_ALL_GROUPS_INFORMATION_NTF = 0x022B

    GW_GET_ALL_GROUPS_INFORMATION_FINISHED_NTF = 0x022C

    GW_GROUP_DELETED_NTF = 0x022D

    GW_HOUSE_STATUS_MONITOR_ENABLE_REQ = 0x0240
    GW_HOUSE_STATUS_MONITOR_ENABLE_CFM = 0x0241

    GW_HOUSE_STATUS_MONITOR_DISABLE_REQ = 0x0242
    GW_HOUSE_STATUS_MONITOR_DISABLE_CFM = 0x0243

    GW_COMMAND_SEND_REQ = 0x0300
    GW_COMMAND_SEND_CFM = 0x0301
    GW_COMMAND_RUN_STATUS_NTF = 0x0302
    GW_COMMAND_REMAINING_TIME_NTF = 0x0303
    GW_SESSION_FINISHED_NTF = 0x0304

    GW_STATUS_REQUEST_REQ = 0x0305
    GW_STATUS_REQUEST_CFM = 0x0306
    GW_STATUS_REQUEST_NTF = 0x0307

    GW_WINK_SEND_REQ = 0x0308
    GW_WINK_SEND_CFM = 0x0309
    GW_WINK_SEND_NTF = 0x030A

    GW_SET_LIMITATION_REQ = 0x0310
    GW_SET_LIMITATION_CFM = 0x0311
    GW_GET_LIMITATION_STATUS_REQ = 0x0312
    GW_GET_LIMITATION_STATUS_CFM = 0x0313
    GW_LIMITATION_STATUS_NTF = 0x0314

    GW_MODE_SEND_REQ = 0x0320
    GW_MODE_SEND_CFM = 0x0321
    GW_MODE_SEND_NTF = 0x0322

    GW_INITIALIZE_SCENE_REQ = 0x0400
    GW_INITIALIZE_SCENE_CFM = 0x0401
    GW_INITIALIZE_SCENE_NTF = 0x0402
    GW_INITIALIZE_SCENE_CANCEL_REQ = 0x0403
    GW_INITIALIZE_SCENE_CANCEL_CFM = 0x0404
    GW_RECORD_SCENE_REQ = 0x0405
    GW_RECORD_SCENE_CFM = 0x0406
    GW_RECORD_SCENE_NTF = 0x0407

    GW_DELETE_SCENE_REQ = 0x0408
    GW_DELETE_SCENE_CFM = 0x0409

    GW_RENAME_SCENE_REQ = 0x040A
    GW_RENAME_SCENE_CFM = 0x040B

    GW_GET_SCENE_LIST_REQ = 0x040C
    GW_GET_SCENE_LIST_CFM = 0x040D
    GW_GET_SCENE_LIST_NTF = 0x040E

    GW_GET_SCENE_INFORMATION_REQ = 0x040F
    GW_GET_SCENE_INFORMATION_CFM = 0x0410
    GW_GET_SCENE_INFORMATION_NTF = 0x0411

    GW_ACTIVATE_SCENE_REQ = 0x0412
    GW_ACTIVATE_SCENE_CFM = 0x0413

    GW_STOP_SCENE_REQ = 0x0415
    GW_STOP_SCENE_CFM = 0x0416

    GW_SCENE_INFORMATION_CHANGED_NTF = 0x0419

    GW_ACTIVATE_PRODUCTGROUP_REQ = 0x0447
    GW_ACTIVATE_PRODUCTGROUP_CFM = 0x0448
    GW_ACTIVATE_PRODUCTGROUP_NTF = 0x0449

    GW_GET_CONTACT_INPUT_LINK_LIST_REQ = 0x0460
    GW_GET_CONTACT_INPUT_LINK_LIST_CFM = 0x0461

    GW_SET_CONTACT_INPUT_LINK_REQ = 0x0462
    GW_SET_CONTACT_INPUT_LINK_CFM = 0x0463

    GW_REMOVE_CONTACT_INPUT_LINK_REQ = 0x0464
    GW_REMOVE_CONTACT_INPUT_LINK_CFM = 0x0465

    GW_GET_ACTIVATION_LOG_HEADER_REQ = 0x0500
    GW_GET_ACTIVATION_LOG_HEADER_CFM = 0x0501

    GW_CLEAR_ACTIVATION_LOG_REQ = 0x0502
    GW_CLEAR_ACTIVATION_LOG_CFM = 0x0503

    GW_GET_ACTIVATION_LOG_LINE_REQ = 0x0504
    GW_GET_ACTIVATION_LOG_LINE_CFM = 0x0505

    GW_ACTIVATION_LOG_UPDATED_NTF = 0x0506

    GW_GET_MULTIPLE_ACTIVATION_LOG_LINES_REQ = 0x0507
    GW_GET_MULTIPLE_ACTIVATION_LOG_LINES_NTF = 0x0508
    GW_GET_MULTIPLE_ACTIVATION_LOG_LINES_CFN = 0x0509

    GW_SET_UTC_REQ = 0x2000
    GW_SET_UTC_CFM = 0x2001

    GW_RTC_SET_TIME_ZONE_REQ = 0x2002
    GW_RTC_SET_TIME_ZONE_CFM = 0x2003

    GW_GET_LOCAL_TIME_REQ = 0x2004
    GW_GET_LOCAL_TIME_CFM = 0x2005

    GW_PASSWORD_ENTER_REQ = 0x3000
    GW_PASSWORD_ENTER_CFM = 0x3001

    GW_PASSWORD_CHANGE_REQ = 0x3002
    GW_PASSWORD_CHANGE_CFM = 0x3003
    GW_PASSWORD_CHANGE_NTF = 0x3004


class Originator(Enum):
    """Enum class for originator."""

    # pylint: disable=line-too-long

    USER = 1                            # User Remote control causing action on actuator
    RAIN = 2                            # Rain sensor
    TIMER = 3                           # Timer controlled
    UPS = 5                             # UPC unit
    SAAC = 8                            # Stand Alone Automatic Controls
    WIND = 9                            # Wind sensor
    LOAD_SHEDDING = 11                  # Managers for requiring a particular electric load shed
    LOCAL_LIGHT = 12                    # Local light sensor
    UNSPECIFIC_ENVIRONMENT_SENSOR = 13  # Used in context with commands transmitted on basis of an unknown sensor for protection of an end-product or house
    EMERGENCY = 255                     # Used in context with emergency or security commands


class Priority(Enum):
    """Enum class for priority."""

    PROTECTION_HUMAN = 0
    PROTECTION_ENVIRONMENT = 1
    USER_LEVEL_1 = 2
    USER_LEVEL_2 = 3
    COMFORT_LEVEL_1 = 4
    COMFORT_LEVEL_2 = 5
    COMFORT_LEVEL_3 = 6
    COMFORT_LEVEL_4 = 7


class LockPriorityLevel(Enum):
    """Enum Class for Lock Priority Level."""

    NO = 0       # Do not lock any priority level.
    MIN30 = 1    # Lock one or more priority level in 30 minutes.
    FOREVER = 2  # Lock one or more priority level forever


class Velocity(Enum):
    """Enum class for velocity."""

    DEFAULT = 0
    SILENT = 1
    FAST = 2
    NOT_AVAILABLE = 255


class NodeTypeWithSubtype(Enum):
    """Enum class for node type plus sub type combined values."""

    # pylint: disable=invalid-name

    NO_TYPE = 0
    INTERIOR_VENETIAN_BLIND = 0x0040
    ROLLER_SHUTTER = 0x0080
    ADJUSTABLE_SLUTS_ROLLING_SHUTTER = 0x0081
    ADJUSTABLE_SLUTS_ROLLING_SHUTTER_WITH_PROJECTION = 0x0082
    VERTICAL_EXTERIOR_AWNING = 0x00C0
    WINDOW_OPENER = 0x0100
    WINDOW_OPENER_WITH_RAIN_SENSOR = 0x0101
    GARAGE_DOOR_OPENER = 0x0140
    LINAR_ANGULAR_POSITION_OF_GARAGE_DOOR = 0x017A
    LIGHT = 0x0180
    LIGHT_ON_OFF = 0x01BA
    GATE_OPENER = 0x01C0
    GATE_OPENER_ANGULAR_POSITION = 0x01FA
    DOOR_LOCK = 0x0240
    WINDOW_LOCK = 0x0241
    VERTICAL_INTERIOR_BLINDS = 0x0280
    DUAL_ROLLER_SHUTTER = 0x0340
    ON_OFF_SWITCH = 0x03C0
    HORIZONTAL_AWNING = 0x0400
    EXTERIOR_VENETIAN_BLIND = 0x0440
    LOUVER_BLIND = 0x0480
    CURTAIN_TRACK = 0x04C0
    VENTILATION_POINT = 0x0500
    VENTILATION_POINT_AIR_INLET = 0x0502
    VENTILATION_POINT_AIR_TRANSFER = 0x0503
    VENTILATION_POINT_AIR_OUTLET = 0x0503
    EXTERIOR_HEATING = 0x0540
    SWINGING_SHUTTERS = 0x0600
    SWINGING_SHUTTER_WITH_INDEPENDENT_LEAVES = 0x0601
    BLADE_OPENER = 0x0740


class NodeType(Enum):
    """Enum class for node types."""

    NO_TYPE = 0
    VENETIAN_BLIND = 1
    ROLLER_SHUTTER = 2
    AWNING = 3
    WINDOW_OPENER = 4
    GARAGE_OPENER = 5
    LIGHT = 6
    GATE_OPENER = 7
    ROLLING_DOOR_OPENER = 8
    LOCK = 9
    BLIND = 10
    SECURE_CONFIGURATION_DEVICE = 11
    BEACON = 12
    DUAL_SHUTTER = 13
    HEATING_TEMPERATURE_INTERFACE = 14
    ON_OFF_SWITCH = 15
    HORIZONTAL_AWNING = 16
    EXTERNAL_VENETIAN_BLIND = 17
    LOUVRE_BLINT = 18
    CURTAIN_TRACK = 19
    VENTILATION_POINT = 20
    EXTERIOR_HEATING = 21
    HEAT_PUMP = 22
    INTRUSION_ALARM = 23
    SWINGING_SHUTTER = 24


class NodeVariation(Enum):
    """Enum class for node variations."""

    NOT_SET = 0
    TOPHUNG = 1
    KIP = 2
    FLAT_ROOT = 3
    SKY_LIGHT = 3


class DHCPParameter(Enum):
    """Enum class for dncp network setup of gateway."""

    DISABLE = 0x00
    ENABLE = 0x01


class GatewayState(Enum):
    """Enum class for state of gateway."""

    TEST_MODE = 0
    GATEWAY_MODE_NO_ACTUATOR = 1
    GATEWAY_MODE_WITH_ACTUATORS = 2
    BEACON_MODE_NOT_CONFIGURED = 3
    BEACON_MODE_CONFIGURED = 4


class GatewaySubState(Enum):
    """Enum class for substate of gateway."""

    IDLE = 0x00
    PERFORMING_TASK_CONFIGURATION_SERVICE_HANDLER = 0x01
    PERFORMING_TASK_SCENE_CONFIGURATION = 0x02
    PERFORMING_TASK_INFORMATION_SERVICE_CONFIGURATION = 0x03
    PERFORMING_TASK_CONTACT_INPUT_CONFIGURATION = 0x04
    PERFORMING_TASK_COMMAND = 0x80
    PERFORMING_TASK_ACTIVATE_GROUP = 0x81
    PERFORMING_TASK_ACTIVATE_SCENE = 0x82
    RESERVED_132 = 0x84   # <-- hey @VELUX: Can you tell us what this value means?


class LeaveLearnStateConfirmationStatus(Enum):
    """Enum class for status leaving Learn state."""

    FAILED = 0
    SUCCESSFUL = 1


class ErrorNumber(Enum):
    """Enum class for Errornumber in GW_ERROR_NTF."""

    UNDEFINED = 0           # Not further defined error.
    WRONG_COMMAND = 1       # Unknown Command or command is not accepted at this state.
    FRAME_ERROR = 2         # ERROR on Frame Structure.
    BUSY = 7                # Busy. Try again later.
    BAD_SYSTABLE_INDEX = 8  # Bad system table index.
    NO_AUTH = 12            # Not authenticated.


class ControllerCopyMode(Enum):
    """Enum class for Copy Controller Mode."""

    # pylint: disable=line-too-long

    TCM = 0  # Transmitting Configuration Mode (TCM): The gateway gets key and system table from another controller.
    RCM = 1  # Receiving Configuration Mode (RCM): The gateway gives key and system table to another controller.


class ControllerCopyStatus(Enum):
    """Enum class for Copy Controller Mode."""

    OK = 0  # OK. Data transfer to or from client controller.
    FAILED_TRANSFER = 1  # Failed. Data transfer to or from client controller interrupted.
    CANCELLED = 4  # Ok. Receiving configuration mode is cancelled in the client controller.
    FAILED_TIMEOUT = 5  # Failed. Timeout.
    FAILED_NOTREADY = 11  # Failed. Configuration service not ready.


class ChangeKeyStatus(Enum):
    """Enum class for Key Change Status."""

    # pylint: disable=line-too-long

    OK_CONTROLLER = 0        # Ok. Key Change in client controller.
    OK_ALL = 2               # Ok. Key change in system table all nodes updated with current key.
    OK_PARTIALLY = 3         # Ok. Key Change in System table. Not all nodes in system table was updated with current key. Check bit array.
    OK_RECEIVED = 5          # Ok. Client controller received a key.
    FAILED_NOTDISABLED = 7   # Failed. Local Stimuli not disabled in all Client System table nodes. See bit array.
    FAILED_NOCONTROLLER = 9  # Failed. Not able to find a controller to get key from.
    FAILED_DTSNOTREADY = 10  # Failed. DTS not ready.
    FAILED_DTSERROR = 11     # Failed. DTS error. At DTS error no key change will take place.
    FAILED_CSNOTREADY = 16   # Failed. CS not ready.


class PgcJobState(Enum):
    """Enum class for Product Generic Configuration Job State."""

    STARTED = 0  # PGC job started
    ENDED = 1    # PGC job ended. Either OK or with error.
    CS_BUSY = 2  # CS busy with other services


class PgcJobStatus(Enum):
    """Enum class for Product Generic Configuration Job Status."""

    OK = 0            # OK - PGC and CS job completed
    OK_PARTIALLY = 1  # Partly success.
    FAILED_PGCCS = 2  # Failed - Error in PGC/CS job.
    FAILED = 3        # Failed - Too long key press or cancel of CS service.


class PgcJobType(Enum):
    """Enum class for Product Generic Configuration Job Type."""

    # pylint: disable=line-too-long

    RECEIVE_ONLY = 0        # Receive system copy or only get key. Short PGC button press.
    RECEIVE_DISTRIBUTE = 1  # Receive key and distribute. Short PGC button press.
    TRANSMIT = 2            # Transmit key (and system). Long PGC button press.
    GENERATE = 3            # Generate new key and distribute or only generate new key. Very long PGC button press.


class DiscoverStatus(Enum):
    """Enum class for Discovery status."""

    # pylint: disable=line-too-long

    OK = 0                 # OK. Discovered nodes. See bit array.
    FAILED_CSNOTREADY = 5  # Failed. CS not ready.
    OK_PARTIALLY = 6       # OK. Same as DISCOVER_NODES_PERFORMED but some nodes were not added to system table (e.g. System table has reached its limit).
    FAILED_CSBUSY = 7      # CS busy with another task.


class PowerMode(Enum):
    """Enum class for Acutuator power Mode."""

    ALWAYS_ALIVE = 0    # ALWAYS_ALIVE
    LOW_POWER_MODE = 1  # LOW_POWER_MODE


class ChangeType(Enum):
    """Enum class Change Type in Group or Scene NTF."""

    DELETED = 0   # Scene or Group deleted
    MODIFIED = 1  # Information modified


class ContactInputAssignement(Enum):
    """Enum class for Contact Input."""

    NOT_ASSINGED = 0   # Input not assigned.
    SCENE = 1          # Scene
    PRODUCT_GROUP = 2  # Product group
    BY_MODE = 3        # One node controlled by mode


class OutputID(Enum):
    """Enum class for Error and Success Output ID."""

    DONT_SEND = 0  # Don’t send any pulse.
    PULSE_PORT_1 = 1  # Send pulse to output port number 1
    PULSE_PORT_2 = 2  # Send pulse to output port number 2
    PULSE_PORT_3 = 3  # Send pulse to output port number 3
    PULSE_PORT_4 = 4  # Send pulse to output port number 4
    PULSE_PORT_5 = 5  # Send pulse to output port number 5


class GroupType(Enum):
    """Enum class for Group Types."""

    USER_GROUP = 0  # The group type is a user group.
    ROOM = 1  # The group type is a Room.
    HOUSE = 2  # The group type is a House.
    ALL_GROUP = 3  # The group type is an All-group.


class LimitationTimer(Enum):
    """Enum class for Limitation Timer."""

    BY_SECONDS = 1      # 1=30 seconds 2=60 seconds 252=7590 seconds
    UNLIMITED = 253     # unlimited
    CLEAR_MASTER = 254  # clear entry for the Master
    CLEAR_ALL = 255     # clear all


class LimitationType(Enum):
    """Enum class for Limitation Types."""

    MIN_LIMITATION = 0  # Resulting minimum limitation.
    MAX_LIMITATION = 1  # Resulting maximum limitation.


class LockTime(Enum):
    """Enum class for Lock Time."""

    BY_SECONDS = 1   # 1=30 seconds, 2=60 seconds .. 254=7650 seconds
    UNLIMITED = 255  # Unlimited time


class WinkTime(Enum):
    """Enum class for Wink Time."""

    STOP = 0                # Stop wink.
    BY_SECONDS = 1          # 1=Wink in 1 sec., 2= Wink in 2 sec. 253=Wink in 253 sec.
    BY_MANUFACTUERER = 254  # Manufacturer specific wink time.
    FOREVER = 255           # Wink forever.


class NodeParameter(Enum):
    """Enum Class for Node Parameter."""

    MP = 0x00       # Main Parameter.
    FP1 = 0x01      # Functional Parameter number 1.
    FP2 = 0x02      # Functional Parameter number 2.
    FP3 = 0x03      # Functional Parameter number 3.
    FP4 = 0x04      # Functional Parameter number 4.
    FP5 = 0x05      # Functional Parameter number 5.
    FP6 = 0x06      # Functional Parameter number 6.
    FP7 = 0x07      # Functional Parameter number 7.
    FP8 = 0x08      # Functional Parameter number 8.
    FP9 = 0x09      # Functional Parameter number 9.
    FP10 = 0x0A     # Functional Parameter number 10.
    FP11 = 0x0B     # Functional Parameter number 11.
    FP12 = 0x0C     # Functional Parameter number 12.
    FP13 = 0x0D     # Functional Parameter number 13.
    FP14 = 0x0E     # Functional Parameter number 14.
    FP15 = 0x0F     # Functional Parameter number 15.
    FP16 = 0x10     # Functional Parameter number 16.
    NOT_USED = 0xFF  # Value to indicate Functional Parameter not used.


class OperatingState(Enum):
    """Enum Class for operating state of the node."""

    NON_EXECUTING = 0
    ERROR_EXECUTING = 1
    NOT_USED = 2
    WAIT_FOR_POWER = 3
    EXECUTING = 4
    DONE = 5
    UNKNOWN = 255


class StatusReply(Enum):
    """Enum Class for Node Status Reply."""

    # pylint: disable=line-too-long

    UNKNOWN_STATUS_REPLY = 0x00                       # Used to indicate unknown reply.
    COMMAND_COMPLETED_OK = 0x01                       # Indicates no errors detected.
    NO_CONTACT = 0x02                                 # Indicates no communication to node.
    MANUALLY_OPERATED = 0x03                          # Indicates manually operated by a user.
    BLOCKED = 0x04                                    # Indicates node has been blocked by an object.
    WRONG_SYSTEMKEY = 0x05                            # Indicates the node contains a wrong system key.
    PRIORITY_LEVEL_LOCKED = 0x06                      # Indicates the node is locked on this priority level.
    REACHED_WRONG_POSITION = 0x07                     # Indicates node has stopped in another position than expected.
    ERROR_DURING_EXECUTION = 0x08                     # Indicates an error has occurred during execution of command.
    NO_EXECUTION = 0x09                               # Indicates no movement of the node parameter.
    CALIBRATING = 0x0A                                # Indicates the node is calibrating the parameters.
    POWER_CONSUMPTION_TOO_HIGH = 0x0B                 # Indicates the node power consumption is too high.
    POWER_CONSUMPTION_TOO_LOW = 0x0C                  # Indicates the node power consumption is too low.
    LOCK_POSITION_OPEN = 0x0D                         # Indicates door lock errors. (Door open during lock command)
    MOTION_TIME_TOO_LONG__COMMUNICATION_ENDED = 0x0E  # Indicates the target was not reached in time.
    THERMAL_PROTECTION = 0x0F                         # Indicates the node has gone into thermal protection mode.
    PRODUCT_NOT_OPERATIONAL = 0x10                    # Indicates the node is not currently operational.
    FILTER_MAINTENANCE_NEEDED = 0x11                  # Indicates the filter needs maintenance.
    BATTERY_LEVEL = 0x12                              # Indicates the battery level is low.
    TARGET_MODIFIED = 0x13                            # Indicates the node has modified the target value of the command.
    MODE_NOT_IMPLEMENTED = 0x14                       # Indicates this node does not support the mode received.
    COMMAND_INCOMPATIBLE_TO_MOVEMENT = 0x15           # Indicates the node is unable to move in the right direction.
    USER_ACTION = 0x16                                # Indicates dead bolt is manually locked during unlock command.
    DEAD_BOLT_ERROR = 0x17                            # Indicates dead bolt error.
    AUTOMATIC_CYCLE_ENGAGED = 0x18                    # Indicates the node has gone into automatic cycle mode.
    WRONG_LOAD_CONNECTED = 0x19                       # Indicates wrong load on node.
    COLOUR_NOT_REACHABLE = 0x1A                       # Indicates that node is unable to reach received colour code.
    TARGET_NOT_REACHABLE = 0x1B                       # Indicates the node is unable to reach received target position.
    BAD_INDEX_RECEIVED = 0x1C                         # Indicates io-protocol has received an invalid index.
    COMMAND_OVERRULED = 0x1D                          # Indicates that the command was overruled by a new command.
    NODE_WAITING_FOR_POWER = 0x1E                     # Indicates that the node reported waiting for power.
    INFORMATION_CODE = 0xDF                           # Indicates an unknown error code received. (Hex code is shown on display)
    PARAMETER_LIMITED = 0xE0                          # Indicates the parameter was limited by an unknown device. (Same as  LIMITATION_BY_UNKNOWN_DEVICE)
    LIMITATION_BY_LOCAL_USER = 0xE1                   # Indicates the parameter was limited by local button.
    LIMITATION_BY_USER = 0xE2                         # Indicates the parameter was limited by a remote control.
    LIMITATION_BY_RAIN = 0xE3                         # Indicates the parameter was limited by a rain sensor.
    LIMITATION_BY_TIMER = 0xE4                        # Indicates the parameter was limited by a timer.
    LIMITATION_BY_UPS = 0xE6                          # Indicates the parameter was limited by a power supply.
    LIMITATION_BY_UNKNOWN_DEVICE = 0xE7               # Indicates the parameter was limited by an unknown device. (Same as PARAMETER_LIMITED)
    LIMITATION_BY_SAAC = 0xEA                         # Indicates the parameter was limited by a standalone automatic controller.
    LIMITATION_BY_WIND = 0xEB                         # Indicates the parameter was limited by a wind sensor.
    LIMITATION_BY_MYSELF = 0xEC                       # Indicates the parameter was limited by the node itself.
    LIMITATION_BY_AUTOMATIC_CYCLE = 0xED              # Indicates the parameter was limited by an automatic cycle.
    LIMITATION_BY_EMERGENCY = 0xEE                    # Indicates the parameter was limited by an emergency.


class StatusId(Enum):
    """Enum Class for Status ID Reply."""

    # pylint: disable=line-too-long

    STATUS_USER = 0x01             # The status is from a user activation.
    STATUS_RAIN = 0x02             # The status is from a rain sensor activation.
    STATUS_TIMER = 0x03            # The status is from a timer generated action.
    STATUS_UPS = 0x05              # The status is from a UPS generated action.
    STATUS_PROGRAM = 0x08          # The status is from an automatic program generated action. (SAAC)
    STATUS_WIND = 0x09             # The status is from a Wind sensor generated action.
    STATUS_MYSELF = 0x0A           # The status is from an actuator generated action.
    STATUS_AUTOMATIC_CYCLE = 0x0B  # The status is from a automatic cycle generated action.
    STATUS_EMERGENCY = 0x0C        # The status is from an emergency or a security generated action.
    STATUS_UNKNOWN = 0xFF          # The status is from from an unknown command originator action.


class RunStatus(Enum):
    """Enum Class for Node Runstatus."""

    EXECUTION_COMPLETED = 0  # Execution is completed with no errors.
    EXECUTION_FAILED = 1     # Execution has failed. (Get specifics in the following error code)
    EXECUTION_ACTIVE = 2     # Execution is still active.


class StatusType(Enum):
    """Enum class for Status Type for GW_STATUS_REQUEST_NTF frame."""

    REQUEST_TARGET_POSITION = 0  # Request Target Position
    REQUEST_CURRENT_POSITION = 1  # Request Current Position
    REQUEST_REMAINING_TIME = 2  # Request Remaining Time
    REQUEST_MAIN_INFO = 3  # Request Main Info
