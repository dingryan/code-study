/**
 * 商品详情页
 */

const api = require('../../utils/api');

Page({
  data: {
    product: null,
    quantity: 1,
    loading: false
  },
  
  onLoad(options) {
    const productId = options.id;
    if (productId) {
      this.loadProduct(productId);
    }
  },
  
  /**
   * 加载商品详情
   */
  async loadProduct(productId) {
    this.setData({ loading: true });
    try {
      const product = await api.get(`/api/products/${productId}`);
      this.setData({ product });
    } catch (error) {
      wx.showToast({ title: error.message || '加载失败', icon: 'none' });
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
    } finally {
      this.setData({ loading: false });
    }
  },
  
  /**
   * 减少数量
   */
  decreaseQuantity() {
    if (this.data.quantity > 1) {
      this.setData({ quantity: this.data.quantity - 1 });
    }
  },
  
  /**
   * 增加数量
   */
  increaseQuantity() {
    const maxQuantity = this.data.product ? this.data.product.stock : 0;
    if (this.data.quantity < maxQuantity) {
      this.setData({ quantity: this.data.quantity + 1 });
    } else {
      wx.showToast({ title: '库存不足', icon: 'none' });
    }
  },
  
  /**
   * 加入购物车
   */
  addToCart() {
    const product = this.data.product;
    if (!product || product.stock <= 0) {
      wx.showToast({ title: '商品缺货', icon: 'none' });
      return;
    }
    
    // 检查登录状态
    const auth = require('../../utils/auth');
    if (!auth.requireLogin()) {
      return;
    }
    
    // 获取购物车数据
    let cart = wx.getStorageSync('cart') || [];
    const existingItem = cart.find(item => item.product_id === product.id);
    
    if (existingItem) {
      existingItem.quantity += this.data.quantity;
    } else {
      cart.push({
        product_id: product.id,
        product_name: product.name,
        product_image: product.image_url,
        price: product.price,
        quantity: this.data.quantity
      });
    }
    
    wx.setStorageSync('cart', cart);
    wx.showToast({ title: '已加入购物车', icon: 'success' });
  },
  
  async buyNow() {
    const product = this.data.product;
    if (!product || product.stock < this.data.quantity) {
      wx.showToast({ title: '库存不足', icon: 'none' });
      return;
    }
    
    // 先保存订单信息到 globalData
    const app = getApp();
    app.globalData.pendingOrder = {
      items: [{
        product_id: product.id,
        product_name: product.name,
        product_image: product.image_url,
        price: product.price,
        quantity: this.data.quantity
      }]
    };
    
    // 检查登录状态
    const auth = require('../../utils/auth');
    if (!auth.requireLogin()) {
      // 未登录，已保存订单信息，跳转到登录页
      return;
    }
    
    // 已登录，直接跳转到订单确认页
    wx.navigateTo({
      url: '/pages/checkout/checkout'
    });
  },
  
  /**
   * 图片加载失败处理
   */
  onImageError() {
    const product = this.data.product;
    if (product) {
      product.image_url = '';
      this.setData({ product });
    }
  }
});

