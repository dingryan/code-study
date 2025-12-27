/** 小程序入口文件 */
App({
  onLaunch() {
    this.checkLogin();
  },
  
  globalData: {
    userInfo: null,
    token: null,
    apiBaseUrl: 'http://localhost:8000',
    pendingOrder: null
  },
  
  checkLogin() {
    const token = wx.getStorageSync('token');
    if (token) {
      this.globalData.token = token;
    }
  }
});

