import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import apiClient from '../utils/api';
import { isAuthenticated, logout } from '../utils/auth';
import './Orders.css';

function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login');
      return;
    }
    loadOrders();
  }, [navigate]);

  const loadOrders = async () => {
    setLoading(true);
    try {
      // 管理员需要获取所有订单，这里可能需要后端添加新的接口
      // 暂时使用用户订单接口，需要后端支持管理员查看所有订单
      const data = await apiClient.get('/api/orders/?skip=0&limit=1000');
      setOrders(data || []);
    } catch (error) {
      alert(error.message || '加载失败');
    } finally {
      setLoading(false);
    }
  };

  const getStatusText = (status) => {
    const statusMap = {
      'pending': '待支付',
      'paid': '已支付',
      'delivered': '已送达',
      'cancelled': '已取消'
    };
    return statusMap[status] || status;
  };

  const getStatusColor = (status) => {
    const colorMap = {
      'pending': '#ff9800',
      'paid': '#4caf50',
      'delivered': '#2196f3',
      'cancelled': '#999'
    };
    return colorMap[status] || '#666';
  };

  return (
    <div className="orders-container">
      <div className="header">
        <h1>订单管理</h1>
        <div className="header-actions">
          <Link to="/change-password" className="change-password-link">修改密码</Link>
          <button onClick={logout} className="logout-btn">退出登录</button>
          <button onClick={loadOrders}>刷新</button>
        </div>
      </div>

      {loading ? (
        <div className="loading">加载中...</div>
      ) : (
        <div className="orders-list">
          {orders.length === 0 ? (
            <div className="empty">暂无订单</div>
          ) : (
            orders.map((order) => (
              <div key={order.id} className="order-card" onClick={() => setSelectedOrder(order)}>
                <div className="order-header">
                  <span className="order-no">订单号: {order.order_no}</span>
                  <span 
                    className="status-badge"
                    style={{ backgroundColor: getStatusColor(order.status) }}
                  >
                    {getStatusText(order.status)}
                  </span>
                </div>
                <div className="order-info">
                  <div>商品数量: {order.items?.length || 0}</div>
                  <div className="total-amount">总金额: ¥{order.total_amount}</div>
                </div>
                <div className="order-time">
                  创建时间: {new Date(order.created_at).toLocaleString()}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {selectedOrder && (
        <div className="modal" onClick={() => setSelectedOrder(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>订单详情</h2>
            <div className="order-detail">
              <div className="detail-item">
                <label>订单号:</label>
                <span>{selectedOrder.order_no}</span>
              </div>
              <div className="detail-item">
                <label>状态:</label>
                <span style={{ color: getStatusColor(selectedOrder.status) }}>
                  {getStatusText(selectedOrder.status)}
                </span>
              </div>
              <div className="detail-item">
                <label>总金额:</label>
                <span className="amount">¥{selectedOrder.total_amount}</span>
              </div>
              {selectedOrder.address && (
                <div className="detail-item">
                  <label>收货地址:</label>
                  <span>
                    {selectedOrder.address.province} {selectedOrder.address.city} {selectedOrder.address.district} {selectedOrder.address.detail}
                  </span>
                </div>
              )}
              {selectedOrder.address && (
                <div className="detail-item">
                  <label>收货人:</label>
                  <span>{selectedOrder.address.name} {selectedOrder.address.phone}</span>
                </div>
              )}
              {selectedOrder.remark && (
                <div className="detail-item">
                  <label>备注:</label>
                  <span>{selectedOrder.remark}</span>
                </div>
              )}
              <div className="detail-item">
                <label>创建时间:</label>
                <span>{new Date(selectedOrder.created_at).toLocaleString()}</span>
              </div>
              <div className="order-items">
                <h3>商品列表</h3>
                {selectedOrder.items?.map((item) => (
                  <div key={item.id} className="order-item">
                    <div className="item-info">
                      <div className="item-name">{item.product_name || `商品ID: ${item.product_id}`}</div>
                      <div className="item-meta">
                        <span>数量: {item.quantity}</span>
                        <span>单价: ¥{item.price}</span>
                        <span>小计: ¥{(item.quantity * item.price).toFixed(2)}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <button onClick={() => setSelectedOrder(null)} className="close-btn">关闭</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Orders;

