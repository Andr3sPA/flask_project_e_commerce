import React, { useState } from 'react';
import axios from 'axios';
import ProtectedComponent from '@/components/protectedComponent'; // Asegúrate de importar tu componente protegido

const LoginComponent = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(null);

  const handleLogin = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/login', {
      email,
      password
    })
    .then(response => {
      setToken(response.data.access_token);
    })
    .catch(error => {
      console.error('Hubo un error al iniciar sesión!', error);
    });
  };

  return (
    <div>
      {!token ? (
        <form onSubmit={handleLogin}>
          <div>
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit">Login</button>
        </form>
      ) : (
        <ProtectedComponent token={token} />
      )}
    </div>
  );
};

export default LoginComponent;
