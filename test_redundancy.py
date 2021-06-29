#!/usr/bin/env python
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.term import makeTerm
if '__main__' == __name__:
    net = Mininet(controller=RemoteController)
    c0 = net.addController('c0',ip="192.168.1.8", port=6633)
    s1 = self.addSwitch('s1', protocols="OpenFlow13")
    s2 = self.addSwitch('s2', protocols="OpenFlow13")
    h1= net.addHost('h1',mac="00:00:00:00:00:01",ip="192.168.1.20/24")
    h2= net.addHost('h2',mac="00:00:00:00:00:02",ip="192.168.1.21/24")
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s2, h1)
    net.addLink(s2, h2)
    #net.addLink(s2, s1)



    h1.cmd('link set h1-eth1 down')
    h1.cmd('ip link set h1-eth1 address 00:00:00:00:00:11')
    h1.cmd('ip addr add 10.1.0.1/24 dev h1-eth1')
    h1.cmd('link set h1-eth1 up')
    h2.cmd('link set h2-eth1 down')
    h2.cmd('ip link set h2-eth1 address 00:00:00:00:00:12')
    h2.cmd('ip addr add 10.1.0.2/24 dev h2-eth1')
    h2.cmd('link set h2-eth1 up')
    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])    
    #net.startTerms()
    CLI(net)
    net.stop()    
    
    
"""
ryu-manager ryu.app.simple_switch_stp_13
h1 ip link set h1-eth1 down 
h1 ip link set h1-eth1 address 00:00:00:00:00:11 
h1 ip addr add 10.1.0.1/8 dev h1-eth1 
h1 ip link set h1-eth1 up
"""
