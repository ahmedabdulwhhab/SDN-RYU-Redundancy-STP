"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.


sudo mn --custom custom_topo_00.py --topo mytopo  --controller remote,ip=127.0.0.1 --switch ovsk,protocols=OpenFlow13 --mac --ipbase=10.1.1.0/24


"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )

        # Add links
        self.addLink( h1, s1 )
        self.addLink( h2, s1 )
        self.addLink( h1, s2 )
        self.addLink( h2, s2 )
   
        """
        h1.cmd('link set h1-eth1 down')
        h1.cmd('ip link set h1-eth1 address 00:00:00:00:00:11')
        h1.cmd('ip addr add 10.1.0.1/24 dev h1-eth1')
        h1.cmd('link set h1-eth1 up')
        h2.cmd('link set h2-eth1 down')
        h2.cmd('ip link set h2-eth1 address 00:00:00:00:00:12')
        h2.cmd('ip addr add 10.1.0.2/24 dev h2-eth1')
        h2.cmd('link set h2-eth1 up')
"""

topos = { 'mytopo': ( lambda: MyTopo() ) }
