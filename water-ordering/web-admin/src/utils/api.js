import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求去重：存储正在进行的请求
const pendingRequests = new Map();

// 生成请求的唯一key
function getRequestKey(config) {
  return `${config.method?.toUpperCase() || 'GET'}_${config.url}_${JSON.stringify(config.data || config.params || {})}`;
}

// 请求拦截器 - 添加token和请求去重
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // 请求去重：如果相同的请求正在进行，取消新请求
    const requestKey = getRequestKey(config);
    if (pendingRequests.has(requestKey)) {
      const cancelToken = pendingRequests.get(requestKey);
      cancelToken.cancel('重复请求已取消');
    }
    
    // 创建取消token并存储
    const cancelTokenSource = axios.CancelToken.source();
    config.cancelToken = cancelTokenSource.token;
    pendingRequests.set(requestKey, cancelTokenSource);
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理错误和清理pending请求
apiClient.interceptors.response.use(
  (response) => {
    // 请求完成，从pending中移除
    const requestKey = getRequestKey(response.config);
    pendingRequests.delete(requestKey);
    
    // 后端返回的数据格式为 { code, msg, data, requestId }
    if (response.data && response.data.code !== undefined) {
      // code为"0"表示成功
      if (response.data.code === "0" || response.data.code === 0) {
        return response.data.data;
      } else {
        // 即使code不是0，也检查msg判断是否成功
        const errorMsg = response.data.msg || response.data.message || '请求失败';
        return Promise.reject(new Error(errorMsg));
      }
    }
    return response.data;
  },
  (error) => {
    // 请求完成（无论成功失败），从pending中移除
    if (error.config) {
      const requestKey = getRequestKey(error.config);
      pendingRequests.delete(requestKey);
    }
    
    // 如果是取消的请求，直接返回
    if (axios.isCancel(error)) {
      return Promise.reject(error);
    }
    
    if (error.response) {
      const { status, data } = error.response;
      if (status === 401) {
        // 未授权，清除token并跳转到登录页
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      } else if (data) {
        const errorMsg = data.msg || data.message || '请求失败';
        return Promise.reject(new Error(errorMsg));
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;

