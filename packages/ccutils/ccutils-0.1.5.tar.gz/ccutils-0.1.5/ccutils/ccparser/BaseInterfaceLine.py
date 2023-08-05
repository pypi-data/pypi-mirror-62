
from ccutils.ccparser import BaseConfigLine
from ccutils.utils import CiscoRange
from ccutils.utils.common_utils import get_logger, split_interface_name
import re


class BaseInterfaceLine(BaseConfigLine):
    """

    """
    _ip_addr_regex = re.compile(pattern=r"^\sip\saddress\s(?P<ip_address>(?:\d{1,3}\.){3}\d{1,3})\s(?P<mask>(?:\d{1,3}\.){3}\d{1,3})(?:\s(?P<secondary>secondary))?", flags=re.MULTILINE)
    _description_regex = re.compile(pattern=r"^\sdescription\s(?P<description>.*)")
    _vrf_regex = re.compile(pattern=r"^(?:\sip)?\svrf\sforwarding\s(?P<vrf>\S+)", flags=re.MULTILINE)
    _shutdown_regex = re.compile(pattern=r"^\sshutdown", flags=re.MULTILINE)
    _ospf_priority_regex = re.compile(pattern=r"^\sip\sospf\spriority\s(?P<ospf_priority>\d+)", flags=re.MULTILINE)
    _cdp_regex = re.compile(pattern=r"cdp enable")
    _logging_event_regex = re.compile(pattern=r"^\slogging\sevent\s(?P<logging_event>\S+)", flags=re.MULTILINE)

    _standby_ip_regex = re.compile(pattern=r"^\sstandby\s(?P<standby_group>\d+)\sip\s(?P<ip_address>(?:\d{1,3}\.){3}\d{1,3})(?:\s(?P<secondary>secondary))?", flags=re.MULTILINE)
    _standby_timers_regex = re.compile(pattern=r"^\sstandby\s(?P<standby_group>\d+)\stimers\s(?P<hello>\d+)\s(?P<hold>\d+)", flags=re.MULTILINE)
    _standby_priority_regex = re.compile(pattern=r"^\sstandby\s(?P<standby_group>\d+)\spriority\s(?P<priority>\d+)", flags=re.MULTILINE)
    _standby_preempt_regex = re.compile(pattern=r"^\sstandby\s(?P<standby_group>\d+)\s(?P<preempt>preempt)", flags=re.MULTILINE)
    _standby_authentication_regex = re.compile(pattern=r"^\sstandby\s(?P<standby_group>\d+)\sauthentication\s(?P<authentication_type>md5)\skey-string\s(?P<key_type>0|7)\s(?P<key_string>\S+)", flags=re.MULTILINE)
    _standby_version_regex = re.compile(pattern=r"^\sstandby\sversion\s(?P<version>2)")
    
    _helper_address_regex = re.compile(pattern=r"^\sip\shelper-address\s(?P<helper_address>(?:\d{1,3}\.){3}\d{1,3})", flags=re.MULTILINE)


    _native_vlan_regex = re.compile(pattern=r"^ switchport trunk native vlan (?P<native_vlan>\d+)", flags=re.MULTILINE)
    _trunk_encapsulation_regex = re.compile(pattern=r"^ switchport trunk encapsulation (?P<encapsulation>dot1q|isl|negotiate)", flags=re.MULTILINE)
    _switchport_mode_regex = re.compile(pattern=r"^ switchport mode (?P<switchport_mode>access|trunk|dot1q-tunnel|private-vlan)")
    _trunk_allowed_vlans_regex = re.compile(pattern=r"^ switchport trunk allowed vlan(?: add)? (?P<allowed_vlans>\S+)", flags=re.MULTILINE)
    _access_vlan_regex = re.compile(pattern=r"^ switchport access vlan (?P<access_vlan>\d+)", flags=re.MULTILINE)
    _voice_vlan_regex = re.compile(pattern=r"^ switchport voice vlan (?P<voice_vlan>\d+)")

    _channel_group_regex = re.compile(pattern=r"^ channel-group (?P<channel_group_number>\d+) mode (?P<channel_group_mode>\S+)")
    _speed_regex = re.compile(pattern=r"^ speed (?P<speed>\d+)", flags=re.MULTILINE)
    _duplex_regex = re.compile(pattern=r"^ duplex (?P<duplex>full|half)", flags=re.MULTILINE)

    _bandwidth_regex = re.compile(pattern=r"^ bandwidth (?P<bandwidth>\d+)", flags=re.MULTILINE)
    _delay_regex = re.compile(pattern=r"^ delay (?P<delay>\d+)", flags=re.MULTILINE)
    _mtu_regex = re.compile(pattern=r"^ mtu (?P<mtu>\d+)", flags=re.MULTILINE)
    _ip_mtu_regex = re.compile(pattern=r"^ ip mtu (?P<ip_mtu>\d+)", flags=re.MULTILINE)
    _ip_tcp_mss_regex = re.compile(pattern=r"^ ip tcp adjust-mss (?P<tcp_mss>\d+)", flags=re.MULTILINE)
    _keepalive_regex = re.compile(pattern=r"^ keepalive (?P<period>\d+) (?P<retries>\d+)")

    _service_policy_regex = re.compile(pattern=r"^ service-policy (?P<direction>input|output) (?P<policy_map>\S+)", flags=re.MULTILINE)
    _tunnel_src_regex = re.compile(pattern=r"^ tunnel source (?P<source>\S+)")
    _tunnel_dest_regex = re.compile(pattern=r"^ tunnel destination (?P<destination>\S+)")
    _tunnel_vrf_regex = re.compile(pattern=r"^ tunnel vrf (?P<vrf>\S+)")
    _tunnel_mode_regex = re.compile(pattern=r"^ tunnel mode (?P<mode>.*?)$")
    _tunnel_ipsec_profile_regex = re.compile(pattern=r"^ tunnel protection ipsec profile (?P<ipsec_profile>\S+)")

    def __init__(self, number, text, config, verbosity):
        """

        :param int number: Index of line in config
        :param str text: Text of the config line
        :param config: Reference to the parent BaseConfigParser object
        :param int verbosity: Logging output level
        """
        super(BaseInterfaceLine, self).__init__(number=number, text=text, config=config, verbosity=verbosity)
        self.logger = get_logger(name="BaseInterfaceLine", verbosity=verbosity)
        

    def get_unprocessed(self, return_type=None):
        unprocessed_children = self.get_children()
        regexes = [
            self._description_regex,
            self._ip_addr_regex,
            self._vrf_regex,
            self._shutdown_regex,
            self._ospf_priority_regex,
            self._cdp_regex,
            self._logging_event_regex,
            self._standby_ip_regex,
            self._standby_timers_regex,
            self._standby_priority_regex,
            self._standby_preempt_regex,
            self._standby_authentication_regex,
            self._standby_version_regex,
            self._helper_address_regex,
            self._native_vlan_regex,
            self._trunk_encapsulation_regex,
            self._switchport_mode_regex,
            self._trunk_allowed_vlans_regex,
            self._access_vlan_regex,
            self._voice_vlan_regex,
            self._channel_group_regex,
            self._speed_regex,
            self._duplex_regex,
            self._bandwidth_regex,
            self._delay_regex,
            self._mtu_regex,
            self._ip_mtu_regex,
            self._ip_tcp_mss_regex,
            self._keepalive_regex,
            self._service_policy_regex,
            self._tunnel_src_regex,
            self._tunnel_dest_regex,
            self._tunnel_vrf_regex,
            self._tunnel_mode_regex,
            self._tunnel_ipsec_profile_regex,
            re.compile(pattern=r"^\sno\sip\saddress", flags=re.MULTILINE),
            re.compile(pattern=r"^ (no )?switchport$", flags=re.MULTILINE),
            re.compile(pattern=r"^ spanning-tree portfast")
        ]
        for regex in regexes:
            for child in self.re_search_children(regex=regex):
                unprocessed_children.remove(child)
        if return_type == "text":
            return [x.text for x in unprocessed_children]

    def _val_to_bool(self, entry, key):
        if entry[key]:
            entry[key] = True
        else:
            entry[key] = False
        return entry

    @property
    def flags(self):
        flags = []
        flags.append(self.port_mode)
        interface = split_interface_name(self.interface_name)
        if "Vlan" in interface[0]:
            flags.append("svi")
        elif "Ethernet" in interface[0]:
            flags.append("physical")
        elif "Port-channel" in interface[0]:
            flags.append("port-channel")
        elif "Tunnel" in interface[0]:
            flags.append("tunnel")
        return flags

    @property
    def interface_name(self):
        """
        Return name of the interface from object.

        :return: Name of the interface
        :rtype: str
        """
        if not self.is_interface:
            return None
        else:
            return self.re_match(self.interface_regex, group=1)

    @property
    def interface_description(self):
        """

        :return: Interface description or `None`
        :rtype: str or `None`
        """
        if not self.is_interface:
            return None
        else:
            regex = r"description\s(.*)"
            candidates = self.re_search_children(regex=self._description_regex, group="description")
            if len(candidates) == 1:
                return candidates[0]
            else:
                return None

    @property
    def port_mode(self):
        if len(self.re_search_children(regex="ip address")):
            return "l3"
        else:
            return "l2"
    
    @property 
    def ip_addresses(self):
        ip_addresses = []
        candidates = self.re_search_children(regex=self._ip_addr_regex)
        for candidate in candidates:
            ip_addresses.append(self._val_to_bool(entry=candidate.re_search(regex=self._ip_addr_regex, group="ALL"), key="secondary"))
        return ip_addresses
        
    @property
    def vrf(self):
        vrf = None
        candidates = self.re_search_children(regex=self._vrf_regex, group="vrf")
        if len(candidates):
            vrf = candidates[0]
        return vrf

    @property
    def shutdown(self):
        if len(self.re_search_children(regex=self._shutdown_regex)):
            return True
        else:
            return False

    @property
    def ospf_priority(self):
        ospf_priority = None
        candidates = self.re_search_children(regex=self._ospf_priority_regex, group="ospf_priority")
        if len(candidates):
            ospf_priority = int(candidates[0])
        return ospf_priority
    
    @property
    def cdp(self):
        global_cdp = self.config.cdp
        candidates = self.re_search_children(regex=self._cdp_regex)
        if len(candidates):
            if "no" in candidates[0].text:
                return False
            else:
                return True
        else:
            return global_cdp

    @property
    def logging_events(self):
        return self.re_search_children(regex=self._logging_event_regex, group="logging_event")

    @property
    def standby(self):
        
        data = {"version": 1}
        if self.re_search_children(regex=self._standby_version_regex, group="version"):
            data["version"] = 2
        standby_ips = [self._val_to_bool(entry=x, key="secondary") for x in self.re_search_children(regex=self._standby_ip_regex, group="ALL")]
        #print(standby_ips)
        standby_timers = self.re_search_children(regex=self._standby_timers_regex, group="ALL")
        #print(standby_timers)
        standby_priority = self.re_search_children(regex=self._standby_priority_regex, group="ALL")
        #print(standby_priority)
        standby_preempt = [self._val_to_bool(entry=x, key="preempt") for x in self.re_search_children(regex=self._standby_preempt_regex, group="ALL")]
        #print(standby_preempt)
        standby_authentication = self.re_search_children(regex=self._standby_authentication_regex, group="ALL")
        #print(standby_authentication)
        if not len(standby_ips):
            return None
        data["groups"] = {}
        for entry in standby_ips:
            if entry["standby_group"] not in data["groups"].keys():
                data["groups"][entry["standby_group"]] = {"ip_addresses": []}
            data["groups"][entry["standby_group"]]["ip_addresses"].append(entry)
        for entry in standby_timers:
            data["groups"][entry["standby_group"]]["hello"] = entry["hello"]
            data["groups"][entry["standby_group"]]["hold"] = entry["hold"]
        for entry in standby_priority:
            data["groups"][entry["standby_group"]]["priority"] = entry["priority"]
        for entry in standby_preempt:
            data["groups"][entry["standby_group"]]["preempt"] = entry["preempt"]
        for entry in standby_authentication:
            data["groups"][entry["standby_group"]]["authentication_type"] = entry["authentication_type"]
            data["groups"][entry["standby_group"]]["key_type"] = entry["key_type"]
            data["groups"][entry["standby_group"]]["key_string"] = entry["key_string"]
        return data

    @property
    def helper_address(self):
        helper_address = None
        candidates = self.re_search_children(regex=self._helper_address_regex, group="helper_address")
        if len(candidates):
            helper_address = candidates
        return helper_address

    @property
    def native_vlan(self):
        native_vlan = None
        candidates = self.re_search_children(regex=self._native_vlan_regex, group="native_vlan")
        if len(candidates):
            native_vlan = int(candidates[0])
        return native_vlan

    @property
    def trunk_encapsulation(self):
        trunk_encapsulation = None
        candidates = self.re_search_children(regex=self._trunk_encapsulation_regex, group="encapsulation")
        if len(candidates):
            trunk_encapsulation = candidates[0]
        return trunk_encapsulation
    
    @property
    def switchport_mode(self):
        switchport_mode = None
        candidates = self.re_search_children(regex=self._switchport_mode_regex, group="switchport_mode")
        if len(candidates):
            switchport_mode = candidates[0]
        return switchport_mode

    @property
    def trunk_allowed_vlans(self):
        candidates = self.re_search_children(regex=self._trunk_allowed_vlans_regex, group="allowed_vlans")
        if len(candidates):
            candidates = ",".join(candidates)
            crange = CiscoRange(text=candidates)
            return crange._list
        else:
            return None
        
    @property
    def access_vlan(self):
        access_vlan = None
        candidates = self.re_search_children(regex=self._access_vlan_regex, group="access_vlan")
        if len(candidates):
            access_vlan = int(candidates[0])
        return access_vlan

    @property
    def voice_vlan(self):
        voice_vlan = None
        candidates = self.re_search_children(regex=self._voice_vlan_regex, group="voice_vlan")
        if len(candidates):
            voice_vlan = int(candidates[0])
        return voice_vlan

    @property
    def channel_group(self):
        channel_group = None
        candidates = self.re_search_children(regex=self._channel_group_regex, group="ALL")
        if len(candidates):
            channel_group = candidates[0]
        return channel_group

    @property
    def speed(self):
        speed = None
        candidates = self.re_search_children(regex=self._speed_regex, group="speed")
        if len(candidates):
            speed = int(candidates[0])
        return speed

    @property
    def duplex(self):
        duplex = None
        candidates = self.re_search_children(regex=self._duplex_regex, group="duplex")
        if len(candidates):
            duplex = candidates[0]
        return duplex

    @property
    def bandwidth(self):
        bandwith = None
        candidates = self.re_search_children(regex=self._bandwidth_regex, group="bandwidth")
        if len(candidates):
            bandwith = candidates[0]
        return bandwith

    @property
    def delay(self):
        delay = None
        candidates = self.re_search_children(regex=self._delay_regex, group="delay")
        if len(candidates):
            delay = candidates[0]
        return delay

    @property
    def mtu(self):
        mtu = None
        candidates = self.re_search_children(regex=self._mtu_regex, group="mtu")
        if len(candidates):
            mtu = int(candidates[0])
        return mtu

    @property
    def ip_mtu(self):
        ip_mtu = None
        candidates = self.re_search_children(regex=self._ip_mtu_regex, group="ip_mtu")
        if len(candidates):
            ip_mtu = int(candidates[0])
        return ip_mtu

    @property
    def tcp_mss(self):
        tcp_mss = None
        candidates = self.re_search_children(regex=self._ip_tcp_mss_regex, group="tcp_mss")
        if len(candidates):
            tcp_mss = int(candidates[0])
        return tcp_mss

    @property
    def keepalive(self):
        keepalive = None
        candidates = self.re_search_children(regex=self._keepalive_regex, group="ALL")
        if len(candidates):
            keepalive = {k: int(v) for k, v in candidates[0].items()}
        return keepalive

    @property
    def service_policy(self):
        service_policy = {"input": None, "output": None}
        candidates = self.re_search_children(regex=self._service_policy_regex, group="ALL")
        for candidate in candidates:
            if candidate["direction"] == "input":
                service_policy["input"] = candidate["policy_map"]
            elif candidate["direction"] == "output":
                service_policy["output"] = candidate["policy_map"]
        print(candidates)
        return service_policy

    @property
    def tunnel_properties(self):
        # Check if interface is a Tunnel
        if not re.match(pattern=r"^Tu", string=self.interface_name):
            return None
        else:
            tunnel_properties = {}
            tunnel_src_candidates = self.re_search_children(regex=self._tunnel_src_regex, group="source")
            tunnel_dest_candidates = self.re_search_children(regex=self._tunnel_dest_regex, group="destination")
            tunnel_vrf_candidates = self.re_search_children(regex=self._tunnel_vrf_regex, group="vrf")
            tunnel_mode_candidates = self.re_search_children(regex=self._tunnel_mode_regex, group="mode")
            tunnel_ipsec_profile_candidates = self.re_search_children(regex=self._tunnel_ipsec_profile_regex, group="ipsec_profile")
            tunnel_properties["source"] = tunnel_src_candidates[0] if tunnel_src_candidates else None
            tunnel_properties["destination"] = tunnel_dest_candidates[0] if tunnel_dest_candidates else None
            tunnel_properties["vrf"] = tunnel_vrf_candidates[0] if tunnel_vrf_candidates else None
            tunnel_properties["mode"] = tunnel_mode_candidates[0] if tunnel_mode_candidates else None
            tunnel_properties["ipsec_profile"] = tunnel_ipsec_profile_candidates[0] if tunnel_ipsec_profile_candidates else None
            return tunnel_properties

    def __str__(self):
        return "[BaseInterfaceLine #{} ({}): '{}']".format(self.number, self.type, self.text)

    def __repr__(self):
        return self.__str__()
