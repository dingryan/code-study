/** API 请求封装 */

const app = getApp();

class ApiClient {
  constructor() {
    this.baseUrl = app.globalData.apiBaseUrl;
  }
  
  request(options) {
    return new Promise((resolve, reject) => {
      const token = wx.getStorageSync('token');
      
      wx.request({
        url: this.baseUrl + options.url,
        method: options.method || 'GET',
        data: options.data || {},
        header: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
          ...options.header
        },
        success: (res) => {
          if (res.statusCode === 200) {
            // 后端返回 code: "0" 表示成功
            if (res.data.code == 0 || res.data.code === "0") {
              resolve(res.data.data);
            } else {
              reject(new Error(res.data.message || res.data.msg || '请求失败'));
            }
          } else if (res.statusCode === 401) {
            this.handleAuthError();
            const errorMsg = res.data.detail || res.data.message || '登录已过期';
            reject(new Error(errorMsg));
          } else if (res.statusCode === 403) {
            const errorMsg = res.data.detail || res.data.message || '权限不足';
            reject(new Error(errorMsg));
          } else {
            const errorMsg = res.data.detail || res.data.message || '请求失败';
            reject(new Error(errorMsg));
          }
        },
        fail: (err) => {
          reject(err);
        }
      });
    });
  }
  
  handleAuthError() {
    wx.removeStorageSync('token');
    app.globalData.token = null;
    app.globalData.userInfo = null;
    wx.reLaunch({
      url: '/pages/index/index'
    });
  }
  
  get(url, data) {
    return this.request({ url, method: 'GET', data });
  }
  
  post(url, data) {
    return this.request({ url, method: 'POST', data });
  }
  
  put(url, data) {
    return this.request({ url, method: 'PUT', data });
  }
  
  patch(url, data) {
    return this.request({ url, method: 'PATCH', data });
  }
  
  delete(url, data) {
    return this.request({ url, method: 'DELETE', data });
  }
}

const api = new ApiClient();
module.exports = api;

