/** 首页 */

const api = require('../../utils/api');
const auth = require('../../utils/auth');
const app = getApp();

Page({
  data: {
    products: [],
    loading: false
  },
  
  onLoad() {
    this.loadProducts();
    this.checkLogin();
  },
  
  onShow() {
    this.loadProducts();
  },
  
  checkLogin() {
    // 首页不需要自动登录，允许未登录用户浏览
    const token = wx.getStorageSync('token');
    if (token) {
      app.globalData.token = token;
    }
  },
  
  async loadProducts() {
    if (this.data.loading) return;
    
    this.setData({ loading: true });
    try {
      const products = await api.get('/api/products/');
      this.setData({ products });
    } catch (error) {
      wx.showToast({ title: error.message || '加载失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
    }
  },
  
  goToProduct(e) {
    const productId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/product/product?id=${productId}`
    });
  },
  
  onPullDownRefresh() {
    this.loadProducts().finally(() => {
      wx.stopPullDownRefresh();
    });
  },
  
  onImageError(e) {
    const index = e.currentTarget.dataset.index;
    const products = this.data.products;
    if (products[index]) {
      products[index].image_url = '';
      this.setData({ products });
    }
  }
});

