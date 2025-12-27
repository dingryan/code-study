/** 图片上传工具 */

const api = require('./api');

/**
 * 选择图片
 */
function chooseImage() {
  return new Promise((resolve, reject) => {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        resolve(res.tempFilePaths[0]);
      },
      fail: (error) => {
        reject(new Error('选择图片失败'));
      }
    });
  });
}

/**
 * 上传图片
 */
async function uploadImage(filePath) {
  try {
    const token = wx.getStorageSync('token');
    if (!token) {
      throw new Error('请先登录');
    }

    wx.showLoading({ title: '上传中...' });
    
    const result = await new Promise((resolve, reject) => {
      wx.uploadFile({
        url: `${getApp().globalData.apiBaseUrl}/api/upload/image`,
        filePath: filePath,
        name: 'file',
        header: {
          'Authorization': `Bearer ${token}`
        },
        success: (res) => {
          try {
            const data = JSON.parse(res.data);
            if (data.code === 200) {
              resolve(data.data);
            } else {
              reject(new Error(data.message || '上传失败'));
            }
          } catch (e) {
            reject(new Error('解析响应失败'));
          }
        },
        fail: (error) => {
          reject(new Error('上传失败'));
        }
      });
    });

    wx.hideLoading();
    
    // 返回完整URL
    const imageUrl = result.url.startsWith('http') 
      ? result.url 
      : `${getApp().globalData.apiBaseUrl}${result.url}`;
    
    return imageUrl;
  } catch (error) {
    wx.hideLoading();
    throw error;
  }
}

/**
 * 选择并上传图片
 */
async function chooseAndUploadImage() {
  try {
    const filePath = await chooseImage();
    const imageUrl = await uploadImage(filePath);
    return imageUrl;
  } catch (error) {
    wx.showToast({ title: error.message || '上传失败', icon: 'none' });
    throw error;
  }
}

/**
 * 预览图片
 */
function previewImage(urls, current) {
  wx.previewImage({
    urls: urls,
    current: current || urls[0]
  });
}

module.exports = {
  chooseImage,
  uploadImage,
  chooseAndUploadImage,
  previewImage
};

