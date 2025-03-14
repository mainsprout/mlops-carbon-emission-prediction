import { GetAxiosInstance } from '../axios/AxiosMethod';

export const fetchLocationInfoByStdlinkid = async (std_link_id) => {
  try {
    // std_link_id를 동적으로 URL에 반영
    const response = await GetAxiosInstance(`http://localhost/api/get_coordinates?std_link_id=${std_link_id}`);

    // 응답 데이터 유효성 검사
    if (response && response.data) {
      return response.data;
    }

    // 데이터가 없을 경우 빈 값 반환
    return { std_link_id: null, coordinates: [] };
  } catch (error) {
    console.error('Failed to fetch location info by std_link_id:', error);
    throw error; // 호출 측에서 에러 처리
  }
};
