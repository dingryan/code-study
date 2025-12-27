/**
 * 购物车页
 */

const api = require('../../utils/api');
const auth = require('../../utils/auth');

Page({
  data: {
    cartItems: [],
    totalAmount: 0,
    selectedAll: false,
    selectedItems: []
  },
  
  onLoad() {
    // 检查登录状态
    if (!auth.requireLogin()) {
      return;
    }
    this.loadCart();
  },
  
  onShow() {
    // 每次显示时刷新购物车
    this.loadCart();
  },
  
  /**
   * 加载购物车
   */
  loadCart() {
    const cart = wx.getStorageSync('cart') || [];
    const cartItems = cart.map(item => ({
      ...item,
      selected: item.selected !== undefined ? item.selected : true
    }));
    const selectedAll = cartItems.length > 0 && cartItems.every(item => item.selected);
    this.setData({ cartItems, selectedAll });
    this.calculateTotal();
  },
  
  calculateTotal() {
    const selectedItems = this.data.cartItems.filter(item => item.selected);
    const total = selectedItems.reduce((sum, item) => {
      return sum + (parseFloat(item.price) * item.quantity);
    }, 0);
    this.setData({ 
      totalAmount: total.toFixed(2),
      selectedItems: selectedItems
    });
  },
  
  toggleSelect(e) {
    const index = e.currentTarget.dataset.index;
    const cartItems = this.data.cartItems;
    cartItems[index].selected = !cartItems[index].selected;
    
    const selectedAll = cartItems.every(item => item.selected);
    
    wx.setStorageSync('cart', cartItems);
    this.setData({ cartItems, selectedAll });
    this.calculateTotal();
  },
  
  toggleSelectAll() {
    const selectedAll = !this.data.selectedAll;
    const cartItems = this.data.cartItems.map(item => ({
      ...item,
      selected: selectedAll
    }));
    
    wx.setStorageSync('cart', cartItems);
    this.setData({ cartItems, selectedAll });
    this.calculateTotal();
  },
  
  /**
   * 更新商品数量
   */
  updateQuantity(e) {
    const index = e.currentTarget.dataset.index;
    const type = e.currentTarget.dataset.type;
    const cartItems = this.data.cartItems;
    
    if (type === 'decrease') {
      if (cartItems[index].quantity > 1) {
        cartItems[index].quantity--;
      } else {
        // 数量为1时，移除商品
        cartItems.splice(index, 1);
      }
    } else if (type === 'increase') {
      cartItems[index].quantity++;
    }
    
    wx.setStorageSync('cart', cartItems);
    this.setData({ cartItems });
    this.calculateTotal();
  },
  
  /**
   * 删除商品
   */
  deleteItem(e) {
    const index = e.currentTarget.dataset.index;
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这个商品吗？',
      success: (res) => {
        if (res.confirm) {
          const cartItems = this.data.cartItems;
          cartItems.splice(index, 1);
          wx.setStorageSync('cart', cartItems);
          this.setData({ cartItems });
          this.calculateTotal();
          wx.showToast({ title: '已删除', icon: 'success' });
        }
      }
    });
  },
  
  async checkout() {
    const selectedItems = this.data.cartItems.filter(item => item.selected);
    if (selectedItems.length === 0) {
      wx.showToast({ title: '请选择要结算的商品', icon: 'none' });
      return;
    }
    
    // 检查登录状态
    if (!auth.requireLogin()) {
      return;
    }
    
    // 保存选中的商品信息到全局
    getApp().globalData.pendingOrder = {
      items: selectedItems.map(item => ({
        product_id: item.product_id,
        product_name: item.product_name,
        product_image: item.product_image,
        quantity: item.quantity,
        price: item.price
      }))
    };
    
    // 跳转到结算页面
    wx.navigateTo({
      url: '/pages/checkout/checkout'
    });
  },
  
  /**
   * 跳转到首页
   */
  goToIndex() {
    wx.switchTab({
      url: '/pages/index/index'
    });
  },
  
  /**
   * 图片加载失败处理
   */
  onImageError(e) {
    const index = e.currentTarget.dataset.index;
    const cartItems = this.data.cartItems;
    if (cartItems[index]) {
      cartItems[index].product_image = '';
      this.setData({ cartItems });
    }
  }
});

