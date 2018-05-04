# shiftboard

This is a rough web service meeting the needs spelled out in the backend engineer coding exercise.

This requires apache and at least one memcached server.

This also relies on perl and the following modules:

..*Cache::Memcached::Fast;
..*CGI qw(:standard);
..*Data::Dumper;
..*Digest::SHA qw(sha1_hex);
..*JSON;
..*LWP::UserAgent;

Caveats:
The unsuccessful external authentication to you service returns the 401 response code and the standard apache response page, on your instructions it said no 'data', if necessary I can remove the page portion. All other server error messages yield just the reponse code and headers and no data.

I did not create a perl module that the api's can call to simplify the memcached calls and the signature verification, but overall it is only a few lines of code.

Per the instructions to return the lastResponse I relied on memcached, the connection of which is in each of the files and only connects to the 127.0.0.1, more servers could be added to this list, at that point I would create a utlity module and let that be used by the scripts.

For apache I used the .htaccess to handle the dispatching for the services, this is easily maintained for a small number of services.

Lastly the curl requests in the exercise instructions left off the '-k' switch to accept my self-rolled certificate. My commands are in the 'test' subdirectory. 

The setup should meet all the requirements of the exercise. 
