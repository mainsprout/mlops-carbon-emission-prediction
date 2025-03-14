import { PostAxiosInstance } from '../axios/AxiosMethod';

export const fetchPredictedData = async ({ creat_de, creat_hm, std_link_id, pasng_spd }) => {
  try {
    // POST 요청으로 변경
    const response = await PostAxiosInstance(
      `http://localhost/traffic_model/predict/`,
      {
        creat_de,
        creat_hm,
        std_link_id,
        pasng_spd,
      }
    );

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
