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
    
    // 检查登录状态
    const auth = require('../../utils/auth');
    if (!auth.requireLogin()) {
      return;
    }
    
    try {
      wx.showLoading({ title: '创建订单中...' });
      
      const addresses = await api.get('/api/addresses/');
      if (!addresses || addresses.length === 0) {
        wx.hideLoading();
        wx.showToast({ title: '请先添加收货地址', icon: 'none' });
        setTimeout(() => {
          wx.navigateTo({
            url: '/pages/address/address'
          });
        }, 1500);
        return;
      }
      
      const address = addresses.find(addr => addr.is_default) || addresses[0];
      
      const orderData = {
        address_id: address.id,
        items: [{
          product_id: product.id,
          quantity: this.data.quantity,
          price: product.price
        }]
      };
      
      const order = await api.post('/api/orders/', orderData);
      wx.hideLoading();
      
      wx.navigateTo({
        url: `/pages/order-detail/order-detail?id=${order.id}`
      });
      
    } catch (error) {
      wx.hideLoading();
      wx.showToast({ title: error.message || '创建订单失败', icon: 'none' });
    }
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

