from ee import Geometry


# def get_pm25(lat: float, lon: float, start_date: str, end_date: str) -> float:
#    point = ee.Geometry.Point([lon, lat])
#    pm25_collection = (ee.ImageCollection('MODIS/061/MCD19A2_GRANULES')
#                       .select('Optical_Depth_047')
#                       .filterDate(start_date, end_date))
#    pm25_mean = (pm25_collection.mean()
#                 .reduceRegion(reducer=ee.Reducer.mean(),
#                               geometry=point, scale=1000))
#    return pm25_mean.getInfo()


def get_bounds_from_coordinates(
    roi_coordinates: list[float], buffer_m: int
) -> Geometry:
    """
    This method creates circular buffer ROI of point that EE converts to bounding box.
    S2Downloader.build_roi deprecated
    """
    return Geometry.Point(roi_coordinates).buffer(buffer_m).bounds()
