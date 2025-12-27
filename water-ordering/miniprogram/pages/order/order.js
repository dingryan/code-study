/**
 * 订单列表页
 */

const api = require('../../utils/api');
const { ORDER_STATUS_TEXT } = require('../../utils/constants');
const auth = require('../../utils/auth');

Page({
  data: {
    orders: [],
    loading: false
  },
  
  onLoad() {
    this.checkLoginAndLoad();
  },
  
  onShow() {
    const token = wx.getStorageSync('token');
    if (token) {
      this.loadOrders();
    } else {
      this.checkLoginAndLoad();
    }
  },
  
  async checkLoginAndLoad() {
    // 检查登录状态
    if (!auth.requireLogin()) {
      return;
    }
    this.loadOrders();
  },
  
  async loadOrders() {
    if (this.data.loading) return;
    
    const token = wx.getStorageSync('token');
    if (!token) {
      return;
    }
    
    this.setData({ loading: true });
    try {
      const orders = await api.get('/api/orders/');
      orders.forEach(order => {
        order.status_text = ORDER_STATUS_TEXT[order.status] || order.status;
      });
      this.setData({ orders });
    } catch (error) {
      if (error.message && error.message.includes('登录')) {
        if (!auth.requireLogin()) {
          return;
        }
        this.loadOrders();
      } else {
        wx.showToast({ title: error.message || '加载失败', icon: 'none' });
      }
    } finally {
      this.setData({ loading: false });
    }
  },
  
  /**
   * 跳转到订单详情
   */
  goToOrderDetail(e) {
    const orderId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/order-detail/order-detail?id=${orderId}`
    });
  },
  
  /**
   * 下拉刷新
   */
  onPullDownRefresh() {
    this.loadOrders().finally(() => {
      wx.stopPullDownRefresh();
    });
  }
});

