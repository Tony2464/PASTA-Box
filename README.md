# PASTA-Box

**P**owerful, **A**dvanced and **S**mart **T**raffic **A**nalyzer

## Requirements

1. secret
Need a folder named "secret" in the root project which contains a file named "secret.py". 
Content example :  
``` text
dbLogin = "adminPasta"  
dBpassword = "PASTA-Box"  
secretKey = "pastaforver"
```  

2.  flask conf

Need a flask conf in the root project :
```text
import sys
#if sys.version_info[0]<3:       # require python3
# raise Exception("Python3 required! Current (wrong) version: '%s'" % sys.version_info)
sys.path.insert(0, '/PASTA-Box/')
from main_api_web import app as application
```

3. WSGID apache2 conf

Need a conf site in `/etc/apache2/sites-available/`, replace USERNAME and GROUP_NAME : 
``` text
<VirtualHost *:80>
 ServerName example.com
 WSGIDaemonProcess flaskapp2 user=USERNAME group=GROUP_NAME threads=5
 WSGIScriptAlias / /PASTA-Box/flaskapp.wsgi
<Directory /PASTA-Box/>
 WSGIProcessGroup flaskapp2
 WSGIApplicationGroup %{GLOBAL}
 WSGIScriptReloading On
 Require all granted
</Directory>
</VirtualHost>
```
