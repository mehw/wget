#!/usr/bin/env python3
from sys import exit
from test.http_test import HTTPTest
from misc.wget_file import WgetFile
import re
import hashlib

"""
    This is to test if Metalink/XML forbids the home path and names
    beginning with the ~ (tilde) character.

    With --trust-server-names, trust the metalink:file names.

    Without --trust-server-names, don't trust the metalink:file names:
    use the basename of --input-metalink, and add a sequential number
    (e.g. .#1, .#2, etc.).

    Strip the directory from unsafe paths.
"""
############# File Definitions ###############################################
bad = "Ouch!"

File1 = "Would you like some Tea?"
File1_lowPref = "Do not take this"
File1_sha256 = hashlib.sha256 (File1.encode ('UTF-8')).hexdigest ()

File2 = "This is gonna be good"
File2_lowPref = "Not this one too"
File2_sha256 = hashlib.sha256 (File2.encode ('UTF-8')).hexdigest ()

File3 = "A little more, please"
File3_lowPref = "That's just too much"
File3_sha256 = hashlib.sha256 (File3.encode ('UTF-8')).hexdigest ()

File4 = "Maybe a biscuit?"
File4_lowPref = "No, thanks"
File4_sha256 = hashlib.sha256 (File4.encode ('UTF-8')).hexdigest ()

File5 = "More Tea...?"
File5_lowPref = "I have to go..."
File5_sha256 = hashlib.sha256 (File5.encode ('UTF-8')).hexdigest ()

MetaXml = \
"""<?xml version="1.0" encoding="utf-8"?>
<metalink version="3.0" xmlns="http://www.metalinker.org/">
  <publisher>
    <name>GNU Wget</name>
  </publisher>
  <license>
    <name>GNU GPL</name>
    <url>http://www.gnu.org/licenses/gpl.html</url>
  </license>
  <identity>Wget Test Files</identity>
  <version>1.2.3</version>
  <description>Wget Test Files description</description>
  <files>
    <file name="~File1"> <!-- rejected by libmetalink -->
      <verification>
        <hash type="sha256">{{FILE1_HASH}}</hash>
      </verification>
      <resources>
        <url type="http" preference="35">http://{{SRV_HOST}}:{{SRV_PORT}}/wrong_file</url>
        <url type="http" preference="40">http://{{SRV_HOST}}:{{SRV_PORT}}/404</url>
        <url type="http" preference="25">http://{{SRV_HOST}}:{{SRV_PORT}}/File1_lowPref</url>
        <url type="http" preference="30">http://{{SRV_HOST}}:{{SRV_PORT}}/File1</url>
      </resources>
    </file>
    <file name="~/File2"> <!-- rejected by libmetalink -->
      <verification>
        <hash type="sha256">{{FILE2_HASH}}</hash>
      </verification>
      <resources>
        <url type="http" preference="35">http://{{SRV_HOST}}:{{SRV_PORT}}/wrong_file</url>
        <url type="http" preference="40">http://{{SRV_HOST}}:{{SRV_PORT}}/404</url>
        <url type="http" preference="25">http://{{SRV_HOST}}:{{SRV_PORT}}/File2_lowPref</url>
        <url type="http" preference="30">http://{{SRV_HOST}}:{{SRV_PORT}}/File2</url>
      </resources>
    </file>
    <file name="dir/~File3"> <!-- rejected by libmetalink -->
      <verification>
        <hash type="sha256">{{FILE3_HASH}}</hash>
      </verification>
      <resources>
        <url type="http" preference="35">http://{{SRV_HOST}}:{{SRV_PORT}}/wrong_file</url>
        <url type="http" preference="40">http://{{SRV_HOST}}:{{SRV_PORT}}/404</url>
        <url type="http" preference="25">http://{{SRV_HOST}}:{{SRV_PORT}}/File3_lowPref</url>
        <url type="http" preference="30">http://{{SRV_HOST}}:{{SRV_PORT}}/File3</url>
      </resources>
    </file>
    <file name="dir/File4~">
      <verification>
        <hash type="sha256">{{FILE4_HASH}}</hash>
      </verification>
      <resources>
        <url type="http" preference="35">http://{{SRV_HOST}}:{{SRV_PORT}}/wrong_file</url>
        <url type="http" preference="40">http://{{SRV_HOST}}:{{SRV_PORT}}/404</url>
        <url type="http" preference="25">http://{{SRV_HOST}}:{{SRV_PORT}}/File4_lowPref</url>
        <url type="http" preference="30">http://{{SRV_HOST}}:{{SRV_PORT}}/File4</url>
      </resources>
    </file>
    <file name="dir/~/File5">
      <verification>
        <hash type="sha256">{{FILE5_HASH}}</hash>
      </verification>
      <resources>
        <url type="http" preference="35">http://{{SRV_HOST}}:{{SRV_PORT}}/wrong_file</url>
        <url type="http" preference="40">http://{{SRV_HOST}}:{{SRV_PORT}}/404</url>
        <url type="http" preference="25">http://{{SRV_HOST}}:{{SRV_PORT}}/File5_lowPref</url>
        <url type="http" preference="30">http://{{SRV_HOST}}:{{SRV_PORT}}/File5</url>
      </resources>
    </file>
  </files>
</metalink>
"""

wrong_file = WgetFile ("wrong_file", bad)

# rejected by libmetalink
File1_orig = WgetFile ("File1", File1)
File1_nono = WgetFile ("File1_lowPref", File1_lowPref)

# rejected by libmetalink
File2_orig = WgetFile ("File2", File2)
File2_nono = WgetFile ("File2_lowPref", File2_lowPref)

# rejected by libmetalink
File3_orig = WgetFile ("File3", File3)
File3_nono = WgetFile ("File3_lowPref", File3_lowPref)

File4_orig = WgetFile ("File4", File4)
File4_down = WgetFile ("test.meta4.#1", File4)
File4_nono = WgetFile ("File4_lowPref", File4_lowPref)

File5_orig = WgetFile ("File5", File5)
File5_down = WgetFile ("test.meta4.#2", File5)
File5_nono = WgetFile ("File5_lowPref", File5_lowPref)

MetaFile = WgetFile ("test.meta4", MetaXml)

WGET_OPTIONS = "--input-metalink test.meta4"
WGET_URLS = [[]]

Files = [[
    wrong_file,
    File1_orig, File1_nono,
    File2_orig, File2_nono,
    File3_orig, File3_nono,
    File4_orig, File4_nono,
    File5_orig, File5_nono
]]
Existing_Files = [MetaFile]

ExpectedReturnCode = 0
ExpectedDownloadedFiles = [
    File4_down,
    File5_down,
    MetaFile
]

################ Pre and Post Test Hooks #####################################
pre_test = {
    "ServerFiles"       : Files,
    "LocalFiles"        : Existing_Files
}
test_options = {
    "WgetCommands"      : WGET_OPTIONS,
    "Urls"              : WGET_URLS
}
post_test = {
    "ExpectedFiles"     : ExpectedDownloadedFiles,
    "ExpectedRetcode"   : ExpectedReturnCode
}

http_test = HTTPTest (
                pre_hook=pre_test,
                test_params=test_options,
                post_hook=post_test,
)

http_test.server_setup()
### Get and use dynamic server sockname
srv_host, srv_port = http_test.servers[0].server_inst.socket.getsockname ()

MetaXml = re.sub (r'{{FILE1_HASH}}', File1_sha256, MetaXml)
MetaXml = re.sub (r'{{FILE2_HASH}}', File2_sha256, MetaXml)
MetaXml = re.sub (r'{{FILE3_HASH}}', File3_sha256, MetaXml)
MetaXml = re.sub (r'{{FILE4_HASH}}', File4_sha256, MetaXml)
MetaXml = re.sub (r'{{FILE5_HASH}}', File5_sha256, MetaXml)
MetaXml = re.sub (r'{{SRV_HOST}}', srv_host, MetaXml)
MetaXml = re.sub (r'{{SRV_PORT}}', str (srv_port), MetaXml)
MetaFile.content = MetaXml

err = http_test.begin ()

exit (err)
