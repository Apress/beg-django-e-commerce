The virtual host files can be used where Apache and NginX are being used together on single machine in order to serve the pages and content of a Django project.

Using these virtual hosts, NginX faces the public and receives all incoming requests, either over HTTP or HTTPS. It any requests to the path /static/ are served from the static directory at the root of the project.

Dynamic requests for Django pages are forwarded to Apache, which is expected to be running on the local machine on port 8080.

Note that both files will require some changes to apply to your own site, hostname, and server machines.
