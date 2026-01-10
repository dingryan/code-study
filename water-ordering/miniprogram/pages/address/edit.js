/** 地址编辑页 */

const api = require('../../utils/api');

Page({
  data: {
    action: 'add',
    addressId: null,
    from: '', // 添加来源标记
    name: '',
    phone: '',
    province: '',
    city: '',
    district: '',
    detail: '',
    isDefault: false
  },
  
  onLoad(options) {
    if (options.action) {
      this.setData({ action: options.action });
    }
    if (options.id) {
      this.setData({ addressId: parseInt(options.id) });
      this.loadAddress();
    }
    // 记录来源页面
    if (options.from) {
      this.setData({ from: options.from });
    }
  },
  
  async loadAddress() {
    try {
      const address = await api.get(`/api/addresses/${this.data.addressId}`);
      this.setData({
        name: address.name || '',
        phone: address.phone || '',
        province: address.province || '',
        city: address.city || '',
        district: address.district || '',
        detail: address.detail || '',
        isDefault: address.is_default || false
      });
    } catch (error) {
      wx.showToast({ title: error.message || '加载失败', icon: 'none' });
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
    }
  },
  
  onNameInput(e) {
    this.setData({ name: e.detail.value });
  },
  
  onPhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },
  
  onProvinceInput(e) {
    this.setData({ province: e.detail.value });
  },
  
  onCityInput(e) {
    this.setData({ city: e.detail.value });
  },
  
  onDistrictInput(e) {
    this.setData({ district: e.detail.value });
  },
  
  onDetailInput(e) {
    this.setData({ detail: e.detail.value });
  },
  
  onDefaultChange(e) {
    this.setData({ isDefault: e.detail.value });
  },
  
  chooseLocation() {
    wx.chooseLocation({
      success: (res) => {
        this.setData({
          province: res.address.split('省')[0] + '省',
          city: res.address.split('市')[0] + '市',
          district: res.address.split('区')[0] + '区',
          detail: res.address
        });
      },
      fail: (err) => {
        console.error('选择位置失败:', err);
      }
    });
  },
  
  validate() {
    if (!this.data.name.trim()) {
      wx.showToast({ title: '请输入收货人姓名', icon: 'none' });
      return false;
    }
    if (!this.data.phone.trim()) {
      wx.showToast({ title: '请输入手机号', icon: 'none' });
      return false;
    }
    if (!/^1[3-9]\d{9}$/.test(this.data.phone)) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' });
      return false;
    }
    if (!this.data.detail.trim()) {
      wx.showToast({ title: '请输入详细地址', icon: 'none' });
      return false;
    }
    return true;
  },
  
  async saveAddress() {
    if (!this.validate()) {
      return;
    }
    
    wx.showLoading({ title: '保存中...' });
    
    try {
      const addressData = {
        name: this.data.name.trim(),
        phone: this.data.phone.trim(),
        province: this.data.province.trim(),
        city: this.data.city.trim(),
        district: this.data.district.trim(),
        detail: this.data.detail.trim(),
        is_default: this.data.isDefault
      };
      
      let newAddress;
      if (this.data.action === 'add') {
        newAddress = await api.post('/api/addresses/', addressData);
        wx.showToast({ title: '添加成功', icon: 'success' });
      } else {
        newAddress = await api.put(`/api/addresses/${this.data.addressId}`, addressData);
        wx.showToast({ title: '更新成功', icon: 'success' });
      }
      
      // 如果来自订单确认页，保存新地址到全局数据
      if (this.data.from === 'checkout' && this.data.action === 'add') {
        getApp().globalData.selectedAddress = newAddress;
      }
      
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
    } catch (error) {
      wx.showToast({ title: error.message || '保存失败', icon: 'none' });
    } finally {
      wx.hideLoading();
    }
  }
});

