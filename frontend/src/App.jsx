import { Button } from "@/components/ui/button"

import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
    const [data, setData] = useState(null);
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMDQ3Njg1OCwianRpIjoiYjIzY2RhYmEtZDVjOS00Zjg3LWI2YzEtYWVmODhmMzZjMDNiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFuZHJlc2RhcmlvLjIwMDFAZ21haWwuY29tIiwibmJmIjoxNzIwNDc2ODU4LCJjc3JmIjoiNDlhNGQ1NWItZDhlMC00MDAzLTkxYjktNWVmNGU3NzE2YjJiIiwiZXhwIjoxNzIwNDc3NzU4fQ.gl_Ct1yFtciR1b0jHuJIZT8RuZXFqheNSuzur7CtmWYeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMDQ4MDQwOCwianRpIjoiZTU2Mjg2NTgtODNkOC00N2Y4LWE2MWYtZmI4ZTBiNDM1NTA3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFuZHJlc2RhcmlvLjIwMDFAZ21haWwuY29tIiwibmJmIjoxNzIwNDgwNDA4LCJjc3JmIjoiOGY3ODRmMWYtOTUzNC00YTc5LTllNzctODMzYjdjMjhkNjE3IiwiZXhwIjoxNzIwNDg0MDA4fQ.IXM-KJ2Av2DE4sH14FdLqqJYcH8_-ztD1yUeVnPSWS4';  // Tu token de acceso aquí
  
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
        console.error('There was an error!', error);
      });
    }, []);
  
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

export default App;
