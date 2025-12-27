import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import apiClient from '../utils/api';
import { isAuthenticated, logout } from '../utils/auth';
import './Products.css';

function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    stock: '',
    image_url: '',
    is_active: true
  });
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login');
      return;
    }
    loadProducts();
  }, [navigate]);

  const loadProducts = async () => {
    setLoading(true);
    try {
      const data = await apiClient.get('/api/products/admin/all');
      setProducts(data || []);
    } catch (error) {
      alert(error.message || '加载失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingProduct) {
        await apiClient.put(`/api/products/${editingProduct.id}`, formData);
        alert('更新成功');
      } else {
        await apiClient.post('/api/products/', formData);
        alert('创建成功');
      }
      setShowForm(false);
      setEditingProduct(null);
      resetForm();
      loadProducts();
    } catch (error) {
      alert(error.message || '操作失败');
    }
  };

  const handleEdit = (product) => {
    setEditingProduct(product);
    setFormData({
      name: product.name || '',
      description: product.description || '',
      price: product.price?.toString() || '',
      stock: product.stock?.toString() || '',
      image_url: product.image_url || '',
      is_active: product.is_active !== false
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!confirm('确定要删除这个商品吗？')) {
      return;
    }
    try {
      await apiClient.delete(`/api/products/${id}`);
      alert('删除成功');
      loadProducts();
    } catch (error) {
      alert(error.message || '删除失败');
    }
  };

  const handleToggle = async (product) => {
    try {
      await apiClient.patch(`/api/products/${product.id}/toggle`, {
        is_active: !product.is_active
      });
      loadProducts();
    } catch (error) {
      alert(error.message || '操作失败');
    }
  };

  const handleUpdateStock = async (product) => {
    const stock = prompt(`当前库存: ${product.stock}\n请输入新库存:`, product.stock);
    if (stock === null) return;
    const stockNum = parseInt(stock);
    if (isNaN(stockNum) || stockNum < 0) {
      alert('请输入有效的库存数量');
      return;
    }
    try {
      await apiClient.patch(`/api/products/${product.id}/stock`, { stock: stockNum });
      alert('更新成功');
      loadProducts();
    } catch (error) {
      alert(error.message || '更新失败');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      price: '',
      stock: '',
      image_url: '',
      is_active: true
    });
  };

  return (
    <div className="products-container">
      <div className="header">
        <h1>商品管理</h1>
        <div className="header-actions">
          <Link to="/change-password" className="change-password-link">修改密码</Link>
          <button onClick={logout} className="logout-btn">退出登录</button>
          <button onClick={() => { setShowForm(true); setEditingProduct(null); resetForm(); }}>
            + 新增商品
          </button>
        </div>
      </div>

      {showForm && (
        <div className="modal">
          <div className="modal-content">
            <h2>{editingProduct ? '编辑商品' : '新增商品'}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>商品名称</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>描述</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={3}
                />
              </div>
              <div className="form-group">
                <label>价格</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>库存</label>
                <input
                  type="number"
                  value={formData.stock}
                  onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>图片URL</label>
                <input
                  type="url"
                  value={formData.image_url}
                  onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>
                  <input
                    type="checkbox"
                    checked={formData.is_active}
                    onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  />
                  上架
                </label>
              </div>
              <div className="form-actions">
                <button type="submit">保存</button>
                <button type="button" onClick={() => { setShowForm(false); setEditingProduct(null); resetForm(); }}>
                  取消
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {loading ? (
        <div className="loading">加载中...</div>
      ) : (
        <div className="products-list">
          {products.map((product) => (
            <div key={product.id} className="product-card">
              <img src={product.image_url || '/placeholder.png'} alt={product.name} />
              <div className="product-info">
                <h3>{product.name}</h3>
                <p>{product.description || '暂无描述'}</p>
                <div className="product-meta">
                  <span className="price">¥{product.price}</span>
                  <span className="stock">库存: {product.stock}</span>
                  <span className={`status ${product.is_active ? 'active' : 'inactive'}`}>
                    {product.is_active ? '上架' : '下架'}
                  </span>
                </div>
              </div>
              <div className="product-actions">
                <button onClick={() => handleEdit(product)}>编辑</button>
                <button onClick={() => handleToggle(product)}>
                  {product.is_active ? '下架' : '上架'}
                </button>
                <button onClick={() => handleUpdateStock(product)}>库存</button>
                <button onClick={() => handleDelete(product.id)} className="delete-btn">删除</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Products;

