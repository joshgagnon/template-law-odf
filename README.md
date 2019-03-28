###Catalex Convert
Generate ODF documents from jinja2 templated ODT files

Local Service
soffice  -env:UserInstallation=file:///tmp/xofficeuser "--accept=socket,port=2002;urp;" --invisible --headless


Production Service
soffice  "--accept=socket,port=2002;urp;" --invisible --headless

