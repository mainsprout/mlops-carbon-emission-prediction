import {GetAxiosInstance} from '../axios/AxiosMethod';

/**
 * Fetches nearby bus stops from the Tmap API.
 * @param {number} lat - Latitude of the center point.
 * @param {number} lng - Longitude of the center point.
 * @param {number} radius - Radius in meters to search for bus stops.
 * @returns {Promise<Array>} - An array of bus stops with their details.
 */
export const fetchBusInfoByRoute = async (startX, startY, endX, endY) => {
  const API_KEY = process.env.REACT_APP_TMAP_API_KEY;
  const url = `/tmap/poi?appKey=${API_KEY}&categories=%EB%B2%84%EC%8A%A4%EC%A0%95%EB%A5%98%EC%9E%A5&centerLat=${lat}&centerLon=${lng}&radius=${radius}`;

  try {
    const response = await GetAxiosInstance(url);
    if (response && response.searchPoiInfo && response.searchPoiInfo.pois) {
      return response.searchPoiInfo.pois.poi || [];
    }
    return [];
  } catch (error) {
    console.error('Failed to fetch nearby bus stops:', error);
    throw error;
  }
};
