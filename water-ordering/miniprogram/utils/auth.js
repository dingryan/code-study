/** 认证相关工具函数 */

const app = getApp();
const api = require('./api');

/**
 * 发送验证码
 */
async function sendCode(phone) {
  try {
    wx.showLoading({ title: '发送中...' });
    const result = await api.post('/api/auth/send-code', { phone });
    wx.hideLoading();
    return result;
  } catch (error) {
    wx.hideLoading();
    throw error;
  }
}

/**
 * 手机号验证码登录
 */
async function phoneLogin(phone, code) {
  try {
    wx.showLoading({ title: '登录中...' });
    const result = await api.post('/api/auth/phone-login', { phone, code });
    
    wx.setStorageSync('token', result.access_token);
    app.globalData.token = result.access_token;
    app.globalData.userInfo = result.user;
    
    wx.hideLoading();
    return result;
  } catch (error) {
    wx.hideLoading();
    throw error;
  }
}

/**
 * 检查登录状态
 */
function checkLogin() {
  const token = wx.getStorageSync('token');
  if (token) {
    app.globalData.token = token;
    return true;
  }
  return false;
}

/**
 * 需要登录时跳转到登录页
 */
function requireLogin() {
  if (!checkLogin()) {
    wx.navigateTo({
      url: '/pages/login/login'
    });
    return false;
  }
  return true;
}

module.exports = {
  sendCode,
  phoneLogin,
  checkLogin,
  requireLogin
};

