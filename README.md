# template-law-odf
Generate ODF documents from jinja2 templated ODT files
soffice  -env:UserInstallation=file:///tmp/xofficeuser "--accept=socket,port=2002;urp;" --invisible --headless
soffice  "--accept=socket,port=2002;urp;" --invisible --headless