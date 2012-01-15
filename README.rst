======================
Python Nagios Frontend
======================

Nagios visualization tool.

.. image:: http://kristianoellegaard.github.com/python-nagios-frontend/ipad-mockup.jpg

Install using pip
---------------------

pip install python-nagios-frontend

Install using puppet
------------------------
https://github.com/dploi/dploi-puppet/blob/master/nagios/manifests/frontend.pp


Configuration
-------------

- The configuration is defined as xml in "/etc/python-nagios-frontend/config.xml".
- Notes for the mk livestatus support 
  (http://mathias-kettner.de/checkmk_livestatus.html):
  The livestatus socket is created with 0660 rights, with nagios user and group
  id. Your webserver/balbec might not be allowed to use the socket. A solution
  is to create a special dir for the socket, owned by the group of your 
  webserver/balbec and by the nagios user and then set the setgid bit on it 
  (the livestatus documentation mentions the sticky bit, but this is wrong).

  mkdir livestatus
  chown nagios:www livestatus
  chmod +s livestatus
  
  The socket, when created within that dir, is created with the 
  balbec/webserver group id and balbec can use it.
- There is an example config file included in the distribution.
- The configuration consists of at least one map holding a combination of 
  several host- or servicegroups.
- A certain combination of displayed hosts can be defined as a precise logical 
  expression. Host- and servicegroups can be combined using "and", "not", and 
  "or" tags.
- Logical operations appear as tags ("<and>...</and>", "<not>...</not>", 
  "<or>...</or>") and can be nested. Several hostgroup entries within a node are
  combined by an implicit "or"
  ("<hostgroup>...<hostgroup/><hostgroup>...<hostgroup/>" is the same as 
  "<or><hostgroup>...<hostgroup/></or><or><hostgroup>...<hostgroup/></or>").
- To hide host- or servicegroups which serve only for filtering purposes the 
  "show" attribute of a hostgroup has to be set to "false".

Example: 

Show all hosts in hostgroups "Level 1" and "Level 2" which appear in hostgroup 
"Section A". "Level 2" hosts which are in hostgroup "Windows" should be omitted.
Also show the servicegroup "HD Space".

<map name="mymap">
  <hostgroup>Level 1</hostgroup>
  <or>
    <hostgroup>Level 2</hostgroup>
    <not>
      <hostgroup show="false">Windows</hostgroup>
    </not>
  </or>
  <and>
    <hostgroup show="false">Section A</hostgroup>
  </and>
  <servicegroup>HD Space</servicegroup>
</map>

Usage:

Use the browser to view the maps in html ("Accept: text/html" in the header) or
use xml for further processing:

curl -s http://balbec

Legacy configuration:

Legacy "config.xml" files (pre v1.3) are supported. Also you can convert them to
the new format by running the supplied "update-config.py" script:

cd /opt/balbec
python ./update-config.py xslt/old_config.xsl old_config.xml > new_config.xml
