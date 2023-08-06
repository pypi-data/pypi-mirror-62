# remotecv_multidir
Multi-directory image loader for RemoteCV which is an OpenCV worker for facial and feature recognition

## Use with Thumbor
This loader is intended to be compatible with the Thumbor Storage when using the `MIXED_STORAGE_FILE_STORAGE = 'thumbor.storages.no_storage'` option and loading files directly from disk.

## Config

Set the following enviroment variables before running RemoteCV:
```
## List of directories to load files from
## defaults to empty list
REMOTECV_MULTIDIR_LOADER_DIRS = []
```

## Running RemoteCV

See [RemoteCV repo](https://github.com/thumbor/remotecv)
or use the Docker container maintaned by [MinimalCompact](https://github.com/MinimalCompact/thumbor/tree/master/remotecv) as a base image... see [/docker/Dockerfile](https://github.com/MinimalCompact/benneic/tree/master/docker) for an example.
