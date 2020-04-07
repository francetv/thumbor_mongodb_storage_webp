#
MongoDB storage adapter for thumbor 7 with auto_webp support Python 3.6 (async).

# Versions

NOT FOR PROD - INTEGRATION RELEASE

This projects uses the following versioning scheme:

`<thumbor major>.<mongodb plugin major>.<mongodb plugin minor>`


# Configuration
```
# MONGO STORAGE OPTIONS
MONGO_STORAGE_SERVER_HOST = 'localhost' # MongoDB storage server host
MONGO_STORAGE_SERVER_PORT = 27017 # MongoDB storage server port
MONGO_STORAGE_SERVER_DB = 'thumbor' # MongoDB storage server database name
MONGO_STORAGE_SERVER_COLLECTION = 'images' # MongoDB storage image collection
MONGO_STORAGE_SERVER_USER = '' # user
MONGO_STORAGE_SERVER_PASSWORD = '' # password
MONGO_STORAGE_SERVER_AUTH = '' # credential stored in this db
MONGO_STORAGE_SERVER_REPLICASET = 'myReplica' # name of the replicaset - option
MONGO_STORAGE_SERVER_READ = 'secondaryPreferred'

# MONGO STORAGE OPTIONS
MONGO_RESULT_STORAGE_SERVER_HOST = 'localhost' # MongoDB storage server host
MONGO_RESULT_STORAGE_SERVER_PORT = 27017 # MongoDB storage server port
MONGO_RESULT_STORAGE_SERVER_DB = 'thumbor' # MongoDB storage server database name
MONGO_RESULT_STORAGE_SERVER_COLLECTION = 'images' # MongoDB storage image collection
MONGO_RESULT_STORAGE_SERVER_USER = '' # user
MONGO_RESULT_STORAGE_SERVER_PASSWORD = '' # password
MONGO_RESULT_STORAGE_SERVER_AUTH = '' # credential stored in this db
MONGO_RESULT_STORAGE_SERVER_REPLICASET = 'myReplica' # name of the replicaset - option
MONGO_RESULT_STORAGE_SERVER_READ = 'secondaryPreferred'
```


Note: avec utilisation de Varnish quelques modifs sont réaliser

Exemple: https://www.fastly.com/blog/test-new-encodings-fastly-including-webp

sub vcl_recv {
  # Normalize Accept, we're only interested in webp right now.
  # And only normalize for URLs we care about.
  if (req.http.Accept && req.url ~ "(\.jpe?g|\.png)($|\?)") {
    # So we don't have to keep using the above regex multiple times.
    set req.http.X-Is-An-Image-URL = "yay";

    # first let's see if it's unacceptable
    if (req.http.Accept ~ "image/webp[^,];q=0(\.0?0?0?)?[^0-9]($|[,;])") {
      unset req.http.Accept;
    }

    # It is acceptable, so if present set to only that
    if (req.http.Accept ~ "image/webp") {
      set req.http.Accept = "image/webp";
    } else {
      # not present, and we don't care about the rest
      unset req.http.Accept;
    }
  }
#FASTLY recv
}

sub vcl_miss {
  # If you have /foo/bar.jpeg, you should also have a /foo/bar.webp

  if (req.http.Accept ~ "image/webp" && req.http.X-Is-An-Image-URL) {
    set bereq.url = regsuball(bereq.url, "(\.jpe?g|\.png)($|\?)", ".webp\2");
  }
#FASTLY miss
}

sub vcl_fetch {
  if (req.http.X-Is-An-Image-URL) {
    if (!beresp.http.Vary ~ "(^|\s|,)Accept($|\s|,)") {
      if (beresp.http.Vary) {
        set beresp.http.Vary = beresp.http.Vary ", Accept";
      } else {
         set beresp.http.Vary = "Accept";
      }
    }
  }
#FASTLY fetch
}