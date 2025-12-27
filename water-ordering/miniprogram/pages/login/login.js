/** 登录页 */

const auth = require('../../utils/auth');

Page({
  data: {
    phone: '',
    code: '',
    countdown: 0,
    codeSent: false,
    devCode: ''  // 开发环境显示的验证码
  },
  
  onLoad() {
    // 如果已登录，返回上一页
    if (auth.checkLogin()) {
      wx.navigateBack();
    }
  },
  
  /**
   * 输入手机号
   */
  onPhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },
  
  /**
   * 输入验证码
   */
  onCodeInput(e) {
    this.setData({ code: e.detail.value });
  },
  
  /**
   * 发送验证码
   */
  async sendCode() {
    const phone = this.data.phone.trim();
    
    // 验证手机号格式
    if (!phone || !/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' });
      return;
    }
    
    if (this.data.countdown > 0) {
      wx.showToast({ title: `请${this.data.countdown}秒后再试`, icon: 'none' });
      return;
    }
    
    try {
      const result = await auth.sendCode(phone);
      
      // 开发环境显示验证码
      if (result.code) {
        this.setData({ 
          codeSent: true,
          devCode: result.code,
          countdown: 60
        });
        wx.showToast({ 
          title: `验证码: ${result.code}`, 
          icon: 'none',
          duration: 3000
        });
      } else {
        this.setData({ 
          codeSent: true,
          countdown: 60
        });
        wx.showToast({ title: '验证码已发送', icon: 'success' });
      }
      
      // 开始倒计时
      this.startCountdown();
      
    } catch (error) {
      wx.showToast({ title: error.message || '发送失败', icon: 'none' });
    }
  },
  
  /**
   * 开始倒计时
   */
  startCountdown() {
    const timer = setInterval(() => {
      if (this.data.countdown <= 1) {
        clearInterval(timer);
        this.setData({ countdown: 0 });
      } else {
        this.setData({ countdown: this.data.countdown - 1 });
      }
    }, 1000);
  },
  
  /**
   * 登录
   */
  async login() {
    const phone = this.data.phone.trim();
    const code = this.data.code.trim();
    
    if (!phone || !/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' });
      return;
    }
    
    if (!code || code.length !== 6) {
      wx.showToast({ title: '请输入6位验证码', icon: 'none' });
      return;
    }
    
    try {
      await auth.phoneLogin(phone, code);
      wx.showToast({ title: '登录成功', icon: 'success' });
      
      // 延迟返回上一页
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
      
    } catch (error) {
      wx.showToast({ title: error.message || '登录失败', icon: 'none' });
    }
  }
});

