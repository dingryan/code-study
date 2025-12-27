/** 结算页 */

const api = require('../../utils/api');
const auth = require('../../utils/auth');

Page({
  data: {
    items: [],
    selectedAddress: null,
    addresses: [],
    totalAmount: 0,
    loading: false
  },
  
  onLoad() {
    this.checkLoginAndLoad();
  },
  
  async checkLoginAndLoad() {
    // 检查登录状态
    if (!auth.requireLogin()) {
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
      return;
    }
    this.loadData();
  },
  
  async loadData() {
    const pendingOrder = getApp().globalData.pendingOrder;
    if (!pendingOrder || !pendingOrder.items) {
      wx.showToast({ title: '订单信息丢失', icon: 'none' });
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
      return;
    }
    
    this.setData({ items: pendingOrder.items });
    this.calculateTotal();
    await this.loadAddresses();
  },
  
  async loadAddresses() {
    try {
      const addresses = await api.get('/api/addresses/');
      if (addresses && addresses.length > 0) {
        const defaultAddress = addresses.find(addr => addr.is_default) || addresses[0];
        this.setData({ 
          addresses,
          selectedAddress: defaultAddress
        });
      }
    } catch (error) {
      wx.showToast({ title: error.message || '加载地址失败', icon: 'none' });
    }
  },
  
  calculateTotal() {
    const total = this.data.items.reduce((sum, item) => {
      return sum + (parseFloat(item.price) * item.quantity);
    }, 0);
    this.setData({ totalAmount: total.toFixed(2) });
  },
  
  selectAddress() {
    wx.navigateTo({
      url: '/pages/address/address?select=true&from=checkout'
    });
  },
  
  onShow() {
    const pages = getCurrentPages();
    const prevPage = pages[pages.length - 2];
    if (prevPage && prevPage.route === 'pages/address/address') {
      const selectedAddress = getApp().globalData.selectedAddress;
      if (selectedAddress) {
        this.setData({ selectedAddress });
        getApp().globalData.selectedAddress = null;
      }
    }
  },
  
  async submitOrder() {
    if (!this.data.selectedAddress) {
      wx.showToast({ title: '请选择收货地址', icon: 'none' });
      return;
    }
    
    if (this.data.items.length === 0) {
      wx.showToast({ title: '订单信息丢失', icon: 'none' });
      return;
    }
    
    if (this.data.loading) return;
    
    this.setData({ loading: true });
    
    try {
      wx.showLoading({ title: '创建订单中...' });
      
      const orderData = {
        address_id: this.data.selectedAddress.id,
        items: this.data.items.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity,
          price: item.price
        }))
      };
      
      const order = await api.post('/api/orders/', orderData);
      wx.hideLoading();
      
      // 清除待创建订单信息
      getApp().globalData.pendingOrder = null;
      
      // 如果是购物车，清除已选中的商品
      const cart = wx.getStorageSync('cart') || [];
      const remainingCart = cart.filter(item => {
        return !this.data.items.some(selectedItem => 
          selectedItem.product_id === item.product_id
        );
      });
      wx.setStorageSync('cart', remainingCart);
      
      wx.redirectTo({
        url: `/pages/order-detail/order-detail?id=${order.id}`
      });
      
    } catch (error) {
      wx.hideLoading();
      wx.showToast({ title: error.message || '创建订单失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
    }
  }
});

