# Data Access Module

Data access module gathers all the data access logic.
Contains:
* `base/source.py` — base abstract class that force construction of classes that are responsible for find, obtain and download data
* `gee` — GEE data access modules:
  - gee_service.py — GEE service/pipeline that combines all steps necessary to download satellite image from Google Earth Engine.
  - image_downloader.py — a function that downloads images from GEE
  - image_info_service.py — contains a class that gets QueryParameters, runs a build ROI function and finds a particular image ID on GEE cloud.
  - orchestrator.py — orchestrates all steps in a clear and readable manner.
  - utils folder — contains helper functions for GEE data access.
    - get_metadata.py — a function that gets metadata from GEE basd on image ID.
    - roi_generator.py — a function that generates ROI based on coordinates and buffer distance in meters.
* `stac` — contains all STAC data access logic. Currently in development.
