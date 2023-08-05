"""Class to create devices from a Dynalite hub."""

import copy
import asyncio
import types

from .const import (
    LOGGER,
    CONF_TEMPLATE_OVERRIDE,
    DEFAULT_COVER_CHANNEL_CLASS,
    DEFAULT_COVER_FACTOR,
    CONF_TRIGGER,
    CONF_FACTOR,
    CONF_CHANNEL_TYPE,
    CONF_HIDDEN_ENTITY,
    CONF_TILT_PERCENTAGE,
    CONF_AREA_OVERRIDE,
    CONF_CHANNEL_CLASS,
    CONF_TEMPLATE,
    CONF_ROOM_ON,
    CONF_ROOM_OFF,
    DEFAULT_TEMPLATES,
    CONF_ROOM,
    DEFAULT_CHANNEL_TYPE,
    CONF_CHANNEL_COVER,
    CONF_NONE,
    CONF_TIME_COVER,
    CONF_OPEN_PRESET,
    CONF_CLOSE_PRESET,
    CONF_STOP_PRESET,
    CONF_DURATION,
    CONF_TILT_TIME,
)
from dynalite_lib import (
    CONF_CHANNEL,
    CONF_AREA,
    CONF_ACTIVE,
    CONF_ACTIVE_ON,
    CONF_ACTIVE_OFF,
    CONF_NAME,
    CONF_PRESET,
    CONF_NODEFAULT,
    EVENT_NEWPRESET,
    EVENT_NEWCHANNEL,
    EVENT_PRESET,
    EVENT_CHANNEL,
    EVENT_CONNECTED,
    EVENT_DISCONNECTED,
    EVENT_CONFIGURED,
    CONF_ACTION,
    CONF_ACTION_REPORT,
    CONF_ACTION_CMD,
    CONF_TRGT_LEVEL,
    CONF_ACT_LEVEL,
    CONF_ALL,
    Dynalite,
)

from .light import DynaliteChannelLightDevice
from .switch import (
    DynaliteChannelSwitchDevice,
    DynalitePresetSwitchDevice,
    DynaliteDualPresetSwitchDevice,
)
from .cover import DynaliteChannelCoverDevice, DynaliteChannelCoverWithTiltDevice, DynaliteTimeCoverDevice, DynaliteTimeCoverWithTiltDevice
from .dynalitebase import DynaliteBaseDevice


class BridgeError(Exception):
    """For errors in the Dynalite bridge."""

    def __init__(self, message):
        """Initialize the exception."""
        self.message = message


class DynaliteDevices:
    """Manages a single Dynalite bridge."""

    def __init__(self, config, loop=None, newDeviceFunc=None, updateDeviceFunc=None):
        """Initialize the system."""
        self.config = copy.deepcopy(config)
        active_val = self.config[CONF_ACTIVE] if CONF_ACTIVE in self.config else CONF_ACTIVE_OFF
        # fix in the case of boolean values
        if active_val is True:
            active_val = CONF_ACTIVE_ON
        elif active_val is False:
            active_val = CONF_ACTIVE_OFF
        self.config[CONF_ACTIVE] = active_val
        self.loop = loop
        self.newDeviceFunc = newDeviceFunc
        self.updateDeviceFunc = updateDeviceFunc
        self.devices = []
        self.waiting_devices = []
        self.configured = False
        self.connected = False
        self.added_presets = {}
        self.added_channels = {}
        self.added_room_switches = {}
        self.added_time_covers = {}
        self.timer_active = False
        self.timer_callbacks = set()

    async def async_setup(self, tries=0):
        """Set up a Dynalite bridge based on host parameter in the config."""
        LOGGER.debug("bridge async_setup - %s", self.config)

        if not self.loop:
            self.loop = asyncio.get_running_loop()

        # insert the templates
        if CONF_TEMPLATE not in self.config:
            LOGGER.debug(CONF_TEMPLATE + " not in config - using defaults")
            self.config[CONF_TEMPLATE] = DEFAULT_TEMPLATES
        else:
            for template in DEFAULT_TEMPLATES:
                if template not in self.config[CONF_TEMPLATE]:
                    LOGGER.debug(
                        "%s not in " + CONF_TEMPLATE + " using default", template
                    )
                    self.config[CONF_TEMPLATE][template] = DEFAULT_TEMPLATES[template]
                else:
                    for param in DEFAULT_TEMPLATES[template]:
                        if param not in self.config[CONF_TEMPLATE][template]:
                            self.config[CONF_TEMPLATE][template][
                                param
                            ] = DEFAULT_TEMPLATES[template][param]
        # add the entities implicitly defined by templates
        for curArea in self.config[CONF_AREA]:
            areaConfig = self.config[CONF_AREA][curArea]
            if CONF_TEMPLATE in areaConfig:
                template = self.config[CONF_AREA][curArea][CONF_TEMPLATE]
                template_params = self.getTemplateParams(curArea)
                if template == CONF_ROOM:
                    areaConfig[CONF_NODEFAULT] = True
                    for conf in [CONF_ROOM_ON, CONF_ROOM_OFF]:
                        self.ensurePresetInConfig(curArea, template_params[conf])
                        areaConfig[conf] = template_params[conf]
                elif template == CONF_TRIGGER:
                    areaConfig[CONF_NODEFAULT] = True
                    self.ensurePresetInConfig(curArea, template_params[CONF_TRIGGER], False, areaConfig[CONF_NAME])
                    areaConfig[CONF_TRIGGER] = template_params[CONF_TRIGGER]
                elif template == CONF_CHANNEL_COVER:
                    areaConfig[CONF_NODEFAULT] = True
                    curChannel = template_params[CONF_CHANNEL]
                    self.ensureChannelInConfig(curArea, curChannel, False, areaConfig[CONF_NAME])
                    areaConfig[CONF_CHANNEL][str(curChannel)][CONF_CHANNEL_TYPE] = "cover"
                    for conf in [CONF_CHANNEL_CLASS, CONF_FACTOR, CONF_TILT_PERCENTAGE]:
                        areaConfig[CONF_CHANNEL][str(curChannel)][conf] = template_params[conf]
                elif template == CONF_TIME_COVER:
                    areaConfig[CONF_NODEFAULT] = True
                    curChannel = template_params[CONF_CHANNEL_COVER]
                    if int(curChannel) > 0:
                        areaConfig[CONF_CHANNEL_COVER] = curChannel
                        self.ensureChannelInConfig(curArea, curChannel)
                    for conf in [CONF_OPEN_PRESET, CONF_CLOSE_PRESET, CONF_STOP_PRESET]:
                        self.ensurePresetInConfig(curArea, template_params[conf])
                        areaConfig[conf] = template_params[conf]
                    for conf in [CONF_CHANNEL_CLASS, CONF_DURATION, CONF_TILT_TIME]:
                        areaConfig[conf] = template_params[conf]
        LOGGER.debug("bridge async_setup (after templates) - %s" % self.config)

        # Configure the dynalite object
        self._dynalite = Dynalite(config=self.config, loop=self.loop)
        eventHandler = self._dynalite.addListener(listenerFunction=self.handleEvent)
        eventHandler.monitorEvent("*")
        newPresetHandler = self._dynalite.addListener(
            listenerFunction=self.handleNewPreset
        )
        newPresetHandler.monitorEvent(EVENT_NEWPRESET)
        presetChangeHandler = self._dynalite.addListener(
            listenerFunction=self.handlePresetChange
        )
        presetChangeHandler.monitorEvent(EVENT_PRESET)
        newChannelHandler = self._dynalite.addListener(
            listenerFunction=self.handleNewChannel
        )
        newChannelHandler.monitorEvent(EVENT_NEWCHANNEL)
        channelChangeHandler = self._dynalite.addListener(
            listenerFunction=self.handleChannelChange
        )
        channelChangeHandler.monitorEvent(EVENT_CHANNEL)
        self._dynalite.start()

        # register the rooms (switches on presets 1/4)
        self.registerRooms()

        # register the time covers
        self.registerTimeCovers()

        return True

    def ensurePresetInConfig(self, area, preset, hidden=True, name=None):
        areaConfig = self.config[CONF_AREA][area]
        if CONF_PRESET not in areaConfig:
            areaConfig[CONF_PRESET] = {}
        if str(preset) not in areaConfig[CONF_PRESET]:
            curConf = {CONF_HIDDEN_ENTITY: hidden}
            if name:
                curConf[CONF_NAME] = name
            areaConfig[CONF_PRESET][str(preset)] = curConf

    def ensureChannelInConfig(self, area, channel, hidden=True, name=None):
        areaConfig = self.config[CONF_AREA][area]
        if CONF_CHANNEL not in areaConfig:
            areaConfig[CONF_CHANNEL] = {}
        if str(channel) not in areaConfig[CONF_CHANNEL]:
            curConf = {CONF_HIDDEN_ENTITY: hidden}
            if name:
                curConf[CONF_NAME] = name
            areaConfig[CONF_CHANNEL][str(channel)] = curConf

    def registerRooms(self):
        """Register the room switches from two normal presets each."""
        for curArea, areaConfig in self.config[CONF_AREA].items():
            if CONF_TEMPLATE in areaConfig and areaConfig[CONF_TEMPLATE] == CONF_ROOM:
                newDevice = DynaliteDualPresetSwitchDevice(
                    curArea,
                    areaConfig[CONF_NAME],
                    areaConfig[CONF_NAME],
                    self.getMasterArea(curArea),
                    self,
                )
                self.added_room_switches[int(curArea)] = newDevice
                self.setPresetIfReady(curArea, areaConfig[CONF_ROOM_ON], 1, newDevice)
                self.setPresetIfReady(curArea, areaConfig[CONF_ROOM_OFF], 2, newDevice)
                self.registerNewDevice("switch", newDevice, False)

    def registerTimeCovers(self):
        """Register the time covers from three presets and a channel each."""
        for curArea, areaConfig in self.config[CONF_AREA].items():
            if CONF_TEMPLATE in areaConfig and areaConfig[CONF_TEMPLATE] == CONF_TIME_COVER:
                if areaConfig[CONF_TILT_TIME] == 0:
                    newDevice = DynaliteTimeCoverDevice(
                        curArea,
                        areaConfig[CONF_NAME],
                        areaConfig[CONF_NAME],
                        areaConfig[CONF_DURATION],
                        areaConfig[CONF_CHANNEL_CLASS],
                        self.getMasterArea(curArea),
                        self,
                    )
                else:
                    newDevice = DynaliteTimeCoverWithTiltDevice(
                        curArea,
                        areaConfig[CONF_NAME],
                        areaConfig[CONF_NAME],
                        areaConfig[CONF_DURATION],
                        areaConfig[CONF_CHANNEL_CLASS],
                        areaConfig[CONF_TILT_TIME],
                        self.getMasterArea(curArea),
                        self,
                    )
                self.added_time_covers[int(curArea)] = newDevice
                self.setPresetIfReady(curArea, areaConfig[CONF_OPEN_PRESET], 1, newDevice)
                self.setPresetIfReady(curArea, areaConfig[CONF_CLOSE_PRESET], 2, newDevice)
                self.setPresetIfReady(curArea, areaConfig[CONF_STOP_PRESET], 3, newDevice)
                if CONF_CHANNEL_COVER in areaConfig:
                    self.setChannelIfReady(curArea, areaConfig[CONF_CHANNEL_COVER], 4, newDevice)
                else:
                    # No channel attached, only presets.
                    dummyDevice = DynaliteBaseDevice(
                        curArea,
                        areaConfig[CONF_NAME],
                        areaConfig[CONF_NAME],
                        self.getMasterArea(curArea),
                        self,
                    )
                    newDevice.set_device(4, dummyDevice)
                self.registerNewDevice("cover", newDevice, False)

    def registerNewDevice(self, category, device, hidden):
        """Register a new device and group all the ones prior to CONFIGURED event together."""
        self.devices.append(device)
        # after initial configuration, every new device gets sent on its own. The initial ones are bunched together
        if not hidden:
            if self.configured:  
                if self.newDeviceFunc:
                    self.newDeviceFunc([device])
            else:  # send all the devices together when configured
                self.waiting_devices.append(device)

    @property
    def available(self):
        """Return whether bridge is available."""
        return self.connected

    def updateDevice(self, device):
        """Update one or more devices."""
        if self.updateDeviceFunc:
            self.updateDeviceFunc(device)

    def getTemplateIndex(self, area, template, conf):
        """Get a specific index from a specific template in an area."""
        # should always be defined either by the user or by the defaults
        # first see if it is in the area
        try:
            return self.config[CONF_AREA][str(area)][conf]
        except KeyError:
            pass
        # next try templateoverride
        try:
            return self.config[CONF_AREA][str(area)][CONF_TEMPLATE_OVERRIDE][conf]
        except KeyError:
            pass
        # next try the template in the config
        # should always be defined either by the user or by the defaults
        my_template = self.config[CONF_TEMPLATE][template]  
        if conf in my_template:
            return my_template[conf]
        # not found
        return None

    def getTemplateParams(self, area):
        """Extract all the parameters of a template."""
        result = {}
        area_config = self.config[CONF_AREA][str(area)]
        template = area_config.get(CONF_TEMPLATE)
        if not template:
            return result
        for conf in self.config[CONF_TEMPLATE][template]:
            value = self.getTemplateIndex(area, template, conf)
            result[conf] = value
        return result

    def setPresetIfReady(self, area, preset, deviceNum, multiDevice):
        """Try to set a preset of a multi device if it was already registered."""
        try:
            device = self.added_presets[int(area)][int(preset)]
            multiDevice.set_device(deviceNum, device)
        except KeyError:
            pass

    def setChannelIfReady(self, area, channel, deviceNum, multiDevice):
        """Try to set a preset of a multi device if it was already registered."""
        try:
            device = self.added_channels[int(area)][int(channel)]
            multiDevice.set_device(deviceNum, device)
        except KeyError:
            pass

    def handleEvent(self, event=None, dynalite=None):
        """Handle all events."""
        LOGGER.debug("handleEvent - type=%s event=%s" % (event.eventType, event.data))
        if event.eventType == EVENT_CONNECTED:
            LOGGER.debug("received CONNECTED message")
            self.connected = True
            self.updateDevice(CONF_ALL)
        elif event.eventType == EVENT_DISCONNECTED:
            LOGGER.debug("received DISCONNECTED message")
            self.connected = False
            self.updateDevice(CONF_ALL)
        elif event.eventType == EVENT_CONFIGURED:
            LOGGER.debug("received CONFIGURED message")
            self.configured = True
            if self.newDeviceFunc and self.waiting_devices:
                self.newDeviceFunc(self.waiting_devices)
                self.waiting_devices = []
        return

    def getMasterArea(self, area):
        """Get the master area when combining entities from different Dynet areas to the same area."""
        if str(area) not in self.config[CONF_AREA]:
            LOGGER.error("getMasterArea - we should not get here")
            raise BridgeError("getMasterArea - area " + str(area) + "is not in config")
        areaConfig = self.config[CONF_AREA][str(area)]
        masterArea = areaConfig[CONF_NAME]
        if CONF_AREA_OVERRIDE in areaConfig:
            overrideArea = areaConfig[CONF_AREA_OVERRIDE]
            masterArea = overrideArea if overrideArea.lower() != CONF_NONE else ""
        return masterArea

    def handleNewPreset(self, event=None, dynalite=None):
        """Register a new preset."""
        LOGGER.debug("handleNewPreset - event=%s", event.data)
        if not hasattr(event, "data"):
            return
        if CONF_AREA not in event.data:
            return
        curArea = event.data[CONF_AREA]
        if CONF_PRESET not in event.data:
            return
        curPreset = event.data[CONF_PRESET]

        if str(curArea) not in self.config[CONF_AREA]:
            LOGGER.debug("adding area " + str(curArea) + " that is not in config")
            self.config[CONF_AREA][str(curArea)] = {CONF_NAME: "Area " + str(curArea)}
        areaConfig = self.config[CONF_AREA][str(curArea)]

        try:
            # If the name is explicitly defined, use it
            presetName = areaConfig[CONF_PRESET][str(curPreset)][CONF_NAME]  
        except KeyError:
            presetName = "Preset " + str(curPreset)
            if CONF_NODEFAULT not in areaConfig or not areaConfig[CONF_NODEFAULT]:
                try:
                    presetName = self.config[CONF_PRESET][str(curPreset)][CONF_NAME]
                except KeyError:
                    pass
        curName = areaConfig[CONF_NAME] + " " + presetName  
        curDevice = self._dynalite.devices[CONF_AREA][curArea].preset[curPreset]
        newDevice = DynalitePresetSwitchDevice(
            curArea,
            areaConfig[CONF_NAME],
            curPreset,
            curName,
            self.getMasterArea(curArea),
            self,
            curDevice,
        )

        try:
            hidden = areaConfig[CONF_PRESET][str(curPreset)][CONF_HIDDEN_ENTITY]
        except KeyError:
            hidden = False

        try:
            # templates may make some elements hidden or register the preset
            template = areaConfig[CONF_TEMPLATE]  
            if template == CONF_ROOM:
                # in a template room, the presets will all be in the room switch
                hidden = True  
                # if it is not there yet, it will be added when the room switch will be created
                if int(curArea) in self.added_room_switches:  
                    multiDevice = self.added_room_switches[int(curArea)]
                    if int(curPreset) == int(areaConfig[CONF_ROOM_ON]):
                        multiDevice.set_device(1, newDevice)
                    if int(curPreset) == int(areaConfig[CONF_ROOM_OFF]):
                        multiDevice.set_device(2, newDevice)
            elif template == CONF_TRIGGER:
                if int(curPreset) != areaConfig[CONF_TRIGGER]:
                    hidden = True
            elif template in [CONF_HIDDEN_ENTITY, CONF_CHANNEL_COVER]:
                hidden = True
            elif template == CONF_TIME_COVER:
                # in a template room, the presets will all be in the time cover
                hidden = True  
                # if it is not there yet, it will be added when the time cover will be created
                if int(curArea) in self.added_time_covers:
                    multiDevice = self.added_time_covers[int(curArea)]
                    if int(curPreset) == int(areaConfig[CONF_OPEN_PRESET]):
                        multiDevice.set_device(1, newDevice)
                    if int(curPreset) == int(areaConfig[CONF_CLOSE_PRESET]):
                        multiDevice.set_device(2, newDevice)
                    if int(curPreset) == int(areaConfig[CONF_STOP_PRESET]):
                        multiDevice.set_device(3, newDevice)
            else:
                LOGGER.error(
                    "Unknown template "
                    + template
                    + ". Should have been caught in config_validation"
                )
        except KeyError:
            pass

        self.registerNewDevice("switch", newDevice, hidden)
        if curArea not in self.added_presets:
            self.added_presets[curArea] = {}
        self.added_presets[curArea][curPreset] = newDevice
        LOGGER.debug(
            "Creating Dynalite preset area=%s preset=%s name=%s hidden=%s", curArea, curPreset, curName, hidden
        )

    def handlePresetChange(self, event=None, dynalite=None):
        """Change the selected preset."""
        LOGGER.debug("handlePresetChange - event=%s" % event.data)
        if not hasattr(event, "data"):
            return
        if CONF_AREA not in event.data:
            return
        curArea = event.data[CONF_AREA]
        if CONF_PRESET not in event.data:
            return

        # Update all the preset devices
        if int(curArea) in self.added_presets:
            for curPresetInArea in self.added_presets[int(curArea)]:
                self.updateDevice(self.added_presets[int(curArea)][curPresetInArea])

    def handleNewChannel(self, event=None, dynalite=None):
        """Register a new channel."""
        LOGGER.debug("handleNewChannel - event=%s" % event.data)
        if not hasattr(event, "data"):
            return
        if CONF_AREA not in event.data:
            return
        curArea = event.data[CONF_AREA]
        if CONF_CHANNEL not in event.data:
            return
        curChannel = event.data[CONF_CHANNEL]

        if str(curArea) not in self.config[CONF_AREA]:
            LOGGER.debug("adding area " + str(curArea) + " that is not in config")
            self.config[CONF_AREA][str(curArea)] = {CONF_NAME: "Area " + str(curArea)}
        areaConfig = self.config[CONF_AREA][str(curArea)]

        try:
            # If the name is explicitly defined, use it
            channelName = areaConfig[CONF_CHANNEL][str(curChannel)][CONF_NAME]  
        except (KeyError, TypeError):
            # If not explicitly defined, use "areaname Channel X"
            channelName = " Channel " + str(curChannel)
        curName = areaConfig[CONF_NAME] + " " + channelName
        curDevice = self._dynalite.devices[CONF_AREA][curArea].channel[curChannel]
        try:
            channelConfig = areaConfig[CONF_CHANNEL][str(curChannel)]
        except KeyError:
            channelConfig = None
        LOGGER.debug("handleNewChannel - channelConfig=%s" % channelConfig)
        channelType = (
            channelConfig[CONF_CHANNEL_TYPE].lower()
            if channelConfig and CONF_CHANNEL_TYPE in channelConfig
            else DEFAULT_CHANNEL_TYPE
        )
        hassArea = self.getMasterArea(curArea)
        hidden = (channelConfig and CONF_HIDDEN_ENTITY in channelConfig and channelConfig[CONF_HIDDEN_ENTITY]) or \
                 (self.config[CONF_AREA][str(curArea)].get(CONF_TEMPLATE) == CONF_HIDDEN_ENTITY)
        if channelType == "light":
            newDevice = DynaliteChannelLightDevice(
                curArea,
                areaConfig[CONF_NAME],
                curChannel,
                curName,
                channelType,
                hassArea,
                self,
                curDevice,
            )
            self.registerNewDevice("light", newDevice, hidden)
        elif channelType == "switch":
            newDevice = DynaliteChannelSwitchDevice(
                curArea,
                areaConfig[CONF_NAME],
                curChannel,
                curName,
                channelType,
                hassArea,
                self,
                curDevice,
            )
            self.registerNewDevice("switch", newDevice, hidden)
        elif channelType == "cover":
            factor = (
                channelConfig[CONF_FACTOR]
                if CONF_FACTOR in channelConfig
                else DEFAULT_COVER_FACTOR
            )
            deviceClass = (
                channelConfig[CONF_CHANNEL_CLASS]
                if CONF_CHANNEL_CLASS in channelConfig
                else DEFAULT_COVER_CHANNEL_CLASS
            )
            if CONF_TILT_PERCENTAGE in channelConfig and channelConfig[CONF_TILTPERCENTAGE] != 0:
                newDevice = DynaliteChannelCoverWithTiltDevice(
                    curArea,
                    areaConfig[CONF_NAME],
                    curChannel,
                    curName,
                    channelType,
                    deviceClass,
                    factor,
                    channelConfig[CONF_TILT_PERCENTAGE],
                    hassArea,
                    self,
                    curDevice,
                )
            else:
                newDevice = DynaliteChannelCoverDevice(
                    curArea,
                    areaConfig[CONF_NAME],
                    curChannel,
                    curName,
                    channelType,
                    deviceClass,
                    factor,
                    hassArea,
                    self,
                    curDevice,
                )
            self.registerNewDevice("cover", newDevice, hidden)
        else:
            LOGGER.info("unknown chnanel type %s - ignoring", channelType)
            return
        if curArea not in self.added_channels:
            self.added_channels[curArea] = {}
        self.added_channels[curArea][curChannel] = newDevice
        LOGGER.debug("Creating Dynalite channel area=%s channel=%s name=%s", curArea, curChannel, curName)
        # if it is a channel from a timecover, register it
        try:
            template = areaConfig[CONF_TEMPLATE]  
            if template == CONF_TIME_COVER:
                # in a template room, the channels will all be in the time cover
                hidden = True  
                # if it is not there yet, it will be added when the time cover will be created
                if int(curArea) in self.added_time_covers:  
                    multiDevice = self.added_time_covers[int(curArea)]
                    if int(curChannel) == int(areaConfig[CONF_CHANNEL_COVER]):
                        multiDevice.set_device(4, newDevice)
        except KeyError:
            pass

    def handleChannelChange(self, event=None, dynalite=None):
        """Change the level of a channel."""
        LOGGER.debug("handleChannelChange - event=%s" % event.data)
        LOGGER.debug("handleChannelChange called event = %s" % event.msg)
        if not hasattr(event, "data"):
            return
        if CONF_AREA not in event.data:
            return
        curArea = event.data[CONF_AREA]
        if CONF_CHANNEL not in event.data:
            return
        curChannel = event.data[CONF_CHANNEL]

        action = event.data[CONF_ACTION]
        if action == CONF_ACTION_REPORT:
            actual_level = (255 - event.data[CONF_ACT_LEVEL]) / 254
            target_level = (255 - event.data[CONF_TRGT_LEVEL]) / 254
        elif action == CONF_ACTION_CMD:
            if CONF_TRGT_LEVEL in event.data:
                target_level = (255 - event.data[CONF_TRGT_LEVEL]) / 254
                # when there is only a "set channel level" command, assume that this is both the actual and the target
                actual_level = target_level
            else: # stop fade command
                try:
                    if curChannel == CONF_ALL:
                        for channel in self.added_channels[int(curArea)]:
                            channelToSet = self.added_channels[int(curArea)][channel]
                            channelToSet.stop_fade()
                            self.updateDevice(channelToSet)  
                    else:
                        channelToSet = self.added_channels[int(curArea)][int(curChannel)]
                        channelToSet.stop_fade()
                        self.updateDevice(channelToSet)  
                except KeyError:
                    pass
                return
        else:
            LOGGER.error("unknown action for channel change %s", action)
            return
        try:
            channelToSet = self.added_channels[int(curArea)][int(curChannel)]
            channelToSet.update_level(actual_level, target_level)
            # to only call if it was already added to ha
            self.updateDevice(channelToSet)  
        except KeyError:
            pass
            
    def add_timer_listener(self, callback_func):
        self.timer_callbacks.add(callback_func)
        if not self.timer_active:
            self.loop.call_later(1, self.timer_func)
            self.timer_active = True
            
    def remove_timer_listener(self, callback_func):
        self.timer_callbacks.discard(callback_func)
        
    def timer_func(self):
        if self.timer_callbacks:
            for callback in self.timer_callbacks:
                self.loop.call_soon(callback)
            self.loop.call_later(1, self.timer_func)
        else:
            self.timer_active = False
        
