import { Button } from "@/components/ui/button"

import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
    const [data, setData] = useState(null);
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMDQ4NDk5NCwianRpIjoiYjc0N2Q2MDUtMmIxZi00ZTkxLTliMDUtZjE3ZDFjZTQ5ZGYzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFuZHJlc2RhcmlvLjIwMDFAZ21haWwuY29tIiwibmJmIjoxNzIwNDg0OTk0LCJjc3JmIjoiNDM2NDYxZTMtYzU3MS00MTg3LTg5MDQtY2JjMzcxOWUwNTFmIiwiZXhwIjoxNzIwNDg4NTk0fQ.3mHR5LVK6wDhnkzwl6kwpSEN8uY63kvzjG1mpBjDpLs';  // Tu token de acceso aquí
  
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
