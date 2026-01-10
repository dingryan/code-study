import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../utils/api';
import { setToken, setUser } from '../utils/auth';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();
  
  // 使用 ref 防止重复请求
  const loadingRef = useRef(false);

  // 错误提示3秒后自动消失
  useEffect(() => {
    if (errorMessage) {
      const timer = setTimeout(() => {
        setErrorMessage('');
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [errorMessage]);

  const handleLogin = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (loading || loadingRef.current) {
      return;
    }
    
    if (!username || !username.trim()) {
      setErrorMessage('请输入用户名');
      return;
    }

    if (!password || !password.trim()) {
      setErrorMessage('请输入密码');
      return;
    }

    loadingRef.current = true;
    setLoading(true);
    setErrorMessage('');
    
    try {
      const result = await apiClient.post('/api/admin-auth/login', { 
        username: username.trim(), 
        password 
      });
      
      console.log('🔍 [Login] 登录响应数据:', result);
      console.log('🔍 [Login] access_token:', result.access_token);
      console.log('🔍 [Login] user:', result.user);
      
      setToken(result.access_token);
      setUser(result.user);
      
      console.log('✅ [Login] Token 已保存到 localStorage');
      console.log('🔍 [Login] 验证保存的 token:', localStorage.getItem('token'));
      
      navigate('/products');
    } catch (error) {
      console.error('❌ [Login] 登录失败:', error);
      setErrorMessage(error.message || '登录失败，请检查用户名和密码');
    } finally {
      setLoading(false);
      loadingRef.current = false;
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>后台管理系统</h1>
        {errorMessage && (
          <div className="error-message">
            {errorMessage}
          </div>
        )}
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>用户名</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="请输入用户名"
              required
              autoFocus
            />
          </div>
          
          <div className="form-group">
            <label>密码</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="请输入密码"
              required
            />
          </div>

          <button type="submit" className="login-btn" disabled={loading || loadingRef.current}>
            {loading ? '登录中...' : '登录'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
