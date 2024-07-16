import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProtectedComponent = ({ token }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/protected', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
      setData(response.data);
    })
    .catch(error => {
      console.error('Hubo un error!', error);
    });
  }, [token]);

  return (
    <div>
      {data ? (
        <div>Logged in as: {data.logged_in_as}</div>
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
};

export default ProtectedComponent;

