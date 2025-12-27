/**
 * 订单详情页
 */

const api = require('../../utils/api');
const { ORDER_STATUS, ORDER_STATUS_TEXT } = require('../../utils/constants');

Page({
  data: {
    order: null,
    loading: false
  },
  
  onLoad(options) {
    const orderId = options.id;
    if (orderId) {
      this.loadOrder(orderId);
    }
  },
  
  /**
   * 加载订单详情
   */
  async loadOrder(orderId) {
    this.setData({ loading: true });
    try {
      const order = await api.get(`/api/orders/${orderId}`);
      order.status_text = ORDER_STATUS_TEXT[order.status] || order.status;
      this.setData({ order });
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
   * 取消订单
   */
  cancelOrder() {
    const order = this.data.order;
    if (!order) return;
    
    if (order.status !== ORDER_STATUS.PENDING) {
      wx.showToast({ title: '订单状态不允许取消', icon: 'none' });
      return;
    }
    
    wx.showModal({
      title: '确认取消',
      content: '确定要取消这个订单吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await api.put(`/api/orders/${order.id}/cancel`);
            wx.showToast({ title: '订单已取消', icon: 'success' });
            this.loadOrder(order.id);
          } catch (error) {
            wx.showToast({ title: error.message || '取消失败', icon: 'none' });
          }
        }
      }
    });
  },
  
  /**
   * 支付订单
   */
  async payOrder() {
    const order = this.data.order;
    if (!order || order.status !== ORDER_STATUS.PENDING) {
      wx.showToast({ title: '订单状态不允许支付', icon: 'none' });
      return;
    }
    
    try {
      wx.showLoading({ title: '支付中...' });
      await api.post('/api/payment/pay', {
        order_id: order.id,
        payment_method: 'wechat'
      });
      wx.hideLoading();
      wx.showToast({ title: '支付成功', icon: 'success' });
      this.loadOrder(order.id);
    } catch (error) {
      wx.hideLoading();
      wx.showToast({ title: error.message || '支付失败', icon: 'none' });
    }
  }
});

