/** 地址管理页 */

const api = require('../../utils/api');
const auth = require('../../utils/auth');

Page({
  data: {
    addresses: [],
    isSelectMode: false
  },
  
  onLoad(options) {
    if (options.select === 'true') {
      this.setData({ isSelectMode: true });
    }
    this.checkLoginAndLoad();
  },
  
  onShow() {
    this.loadAddresses();
  },
  
  async checkLoginAndLoad() {
    const token = wx.getStorageSync('token');
    if (!token) {
      try {
        await auth.wechatLogin();
      } catch (error) {
        wx.showToast({ title: '请先登录', icon: 'none' });
        return;
      }
    }
    this.loadAddresses();
  },
  
  async loadAddresses() {
    try {
      const addresses = await api.get('/api/addresses/');
      this.setData({ addresses });
    } catch (error) {
      wx.showToast({ title: error.message || '加载失败', icon: 'none' });
    }
  },
  
  addAddress() {
    wx.navigateTo({
      url: '/pages/address/edit?action=add'
    });
  },
  
  editAddress(e) {
    const addressId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/address/edit?action=edit&id=${addressId}`
    });
  },
  
  deleteAddress(e) {
    const addressId = e.currentTarget.dataset.id;
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这个地址吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await api.delete(`/api/addresses/${addressId}`);
            wx.showToast({ title: '删除成功', icon: 'success' });
            this.loadAddresses();
          } catch (error) {
            wx.showToast({ title: error.message || '删除失败', icon: 'none' });
          }
        }
      }
    });
  },
  
  selectAddress(e) {
    if (!this.data.isSelectMode) return;
    
    const addressId = e.currentTarget.dataset.id;
    const address = this.data.addresses.find(addr => addr.id === addressId);
    if (!address) return;
    
    const pages = getCurrentPages();
    const prevPage = pages[pages.length - 2];
    
    if (prevPage && typeof prevPage.selectAddress === 'function') {
      prevPage.selectAddress(address);
      wx.navigateBack();
    } else if (prevPage && prevPage.route === 'pages/checkout/checkout') {
      // 从结算页面来的，保存地址到全局
      getApp().globalData.selectedAddress = address;
      wx.navigateBack();
    } else {
      // 如果没有回调函数，直接创建订单
      this.createOrderWithSelectedAddress(address);
    }
  },
  
  /**
   * 使用选中的地址创建订单（当没有回调函数时）
   */
  async createOrderWithSelectedAddress(address) {
    const pendingOrder = getApp().globalData.pendingOrder;
    if (!pendingOrder) {
      wx.showToast({ title: '订单信息丢失', icon: 'none' });
      wx.navigateBack();
      return;
    }
    
    try {
      wx.showLoading({ title: '创建订单中...' });
      const api = require('../../utils/api');
      
      const orderData = {
        address_id: address.id,
        items: pendingOrder.items || [pendingOrder]
      };
      
      const order = await api.post('/api/orders/', orderData);
      wx.hideLoading();
      
      // 清除待创建订单信息
      getApp().globalData.pendingOrder = null;
      
      // 如果是购物车，清除购物车
      const pages = getCurrentPages();
      const prevPage = pages[pages.length - 2];
      if (prevPage && prevPage.route === 'pages/cart/cart') {
        wx.removeStorageSync('cart');
      }
      
      // 跳转到订单详情
      wx.redirectTo({
        url: `/pages/order-detail/order-detail?id=${order.id}`
      });
      
    } catch (error) {
      wx.hideLoading();
      wx.showToast({ title: error.message || '创建订单失败', icon: 'none' });
    }
  }
});

