# Developer documentation

## Password file INI format

    [ entry_name ]   # free string
    connection_name: either FQDN, URL, SSID, URI # currently on wishlist
    user:
    password:
    help:            # aka "mnemonic"
    description:
    eid:             # SHA1 hash, calculated from the other info


### Examples

Root user on a Linux/Unix system:

    [ Papa Smurf (Root) ]
    connection_name: papa.smurf.smurf
    user: root
    password: Mh4_l,ifw2as
    help: Mary had a little lamb, its fleece was white as snow
    description: Root access to main smurf computer

MySQL user:

    [ Smurfette DB (MySQL) ]
    connection_name: smurfette_db.smurf.smurf
    user: root
    password: Lah,5la,lah,4la
    help: Lah lah, la la la la, lah, la la la la
    description: Admin access to Smurfette database

GitHub:

    [ Brainy GitHub ]
    connection_name: http://github.com
    user: brainy_smurf
    password: Hmf=iP5?
    help: How much further is it Papa Smurf?
    description: Brainy's account on http://github.com

Wireless internet in a coffee shop:

    [ Hefty Smurf's Heavy Coffee ]
    ssid: HeftyCoffee
    password: smurfilischous
    description: Access info for Hefty's wireless internet
