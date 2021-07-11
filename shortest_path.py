from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3, ofproto_v1_3_parser
from ryu.controller.handler import set_ev_cls
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller import ofp_event
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.topology import event
from ryu.topology.api import get_switch, get_link
import networkx as nx # To install it yourself, install version 1.11
 
 
 # Source: https://blog.csdn.net/qq_37041925/article/details/84838848
 
class ExampleShortestForwarding(app_manager.RyuApp):
    """docstring for ClassName"""
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
 
    def __init__(self, *args, **kwargs):
        super(ExampleShortestForwarding, self).__init__(*args, **kwargs)
        self.topology_api_app = self # ie for myself
        self.network = nx.DiGraph() # Digraph indicates a directed graph
        self.paths = {}
 
    # handle switch features in packets
 
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
 
        # install a table-miss flow entry for each datapath
        match = ofp_parser.OFPMatch()
        actions = [ofp_parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                              ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
 
    # install flow entry
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
 
        inst = [ofp_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                 actions)]
        mod = ofp_parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)
 
    @set_ev_cls(event.EventSwitchEnter, [CONFIG_DISPATCHER, MAIN_DISPATCHER])
    def get_topology(self, ev):
        # get nodes
        switch_list = get_switch(self.topology_api_app, None)
        switches = [switch.dp.id for switch in switch_list]  # del self
        self.network.add_nodes_from(switches)
 
        # get links
        links_list = get_link(self.topology_api_app, None)
        links = [(link.src.dpid, link.dst.dpid, {
                  'port': link.src.port_no}) for link in links_list]
        self.network.add_edges_from(links)
 
        # get reverse links
        links = [(link.dst.dpid, link.src.dpid, {
                  'port': link.dst.port_no}) for link in links_list]
  # too many unpacket
        self.network.add_edges_from(links)
    # get out_port by using networkx's Dijkstra algorithm.
 
    def get_out_port(self, datapath, src, dst, in_port):
        dpid = datapath.id
        # add links between host and access  switch
        if src not in self.network:
            self.network.add_node(src)
            Self.network.add_edge(dpid, src, port=in_port) #switch to host
            Self.network.add_edge(src, dpid) # Host to switch, the port is meaningless at this time
            self.paths.setdefault(src, {})
