import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器 - 添加token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器 - 统一处理响应
apiClient.interceptors.response.use(
  (response) => {
    // 后端统一返回格式: { code, msg, data, requestId }
    if (response.data && response.data.code !== undefined) {
      // code为"0"表示成功
      if (response.data.code === "0" || response.data.code === 0) {
        return response.data.data;
      } else {
        const errorMsg = response.data.msg || response.data.message || '请求失败';
        return Promise.reject(new Error(errorMsg));
      }
    }
    return response.data;
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response;
      
      if (status === 401) {
        // 未授权，清除token并跳转到登录页
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      } else if (data) {
        const errorMsg = data.msg || data.message || data.detail || '请求失败';
        return Promise.reject(new Error(errorMsg));
      }
    } else if (error.request) {
      return Promise.reject(new Error('网络连接失败，请检查后端服务是否启动'));
    }
    return Promise.reject(error);
  }
);

export default apiClient;
