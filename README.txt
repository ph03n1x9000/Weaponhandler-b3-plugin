Weaponhandler-b3-plugin
=======================

## Description:

Warns or kicks players who are using restricted weapons.
This plugin has only been tested in Call of Duty 4. Any feedback on other CoD releases would be appreciated.


## Installation:

1) Copy weaponhandler.py to b3/extplugins
2) Copy weaponhandler.xml to b3/extplugins/conf
3) Add the following line to b3.xml
----------
<plugin name="weaponhandler" config="@b3/extplugins/conf/weaponhandler.xml" />
----------



=========================================
KNOWN ISSUES:

# Geowelcome Plugin breaks the functions of this plugin due to the time delay in Geowelcome's messages;
If the game server has players connecting and disconnecting quickly (popular or high traffic servers), 
Geowelcome is caught up processing several player welcome messages. 
If this plugin is supposed to penalize a player while Geowelcome is processing messages, 
the penalty may not work. -- Solution: Use Location plugin instead of Geowelcome --
