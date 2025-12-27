/**
 * 个人中心页
 */

const api = require('../../utils/api');
const auth = require('../../utils/auth');

Page({
  data: {
    userInfo: null
  },
  
  onLoad() {
    this.loadUserInfo();
  },
  
  onShow() {
    this.loadUserInfo();
  },
  
  /**
   * 加载用户信息
   */
  async loadUserInfo() {
    const token = wx.getStorageSync('token');
    if (!token) {
      return;
    }
    
    try {
      const userInfo = await api.get('/api/users/me');
      this.setData({ userInfo });
    } catch (error) {
      console.error('加载用户信息失败:', error);
    }
  },
  
  /**
   * 跳转到地址管理
   */
  goToAddress() {
    wx.navigateTo({
      url: '/pages/address/address'
    });
  },
  
  /**
   * 退出登录
   */
  logout() {
    wx.showModal({
      title: '确认退出',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          wx.removeStorageSync('token');
          getApp().globalData.token = null;
          getApp().globalData.userInfo = null;
          wx.reLaunch({
            url: '/pages/index/index'
          });
        }
      }
    });
  }
});

