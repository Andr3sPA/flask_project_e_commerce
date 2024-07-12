import { Button } from "@/components/ui/button"
import {LoginForm} from "@/components/login"
import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [isShown, setIsShown] = useState(false);

  const handleClick = () => {
    setIsShown(!isShown); // Toggle the isShown state
  };
  const handleLogout = async (e) => {



        const response = await axios.get('http://localhost:5000/logout',{ withCredentials: true }).then(response => {
          // handle success
          console.log(response.data);
        })
        .catch(error => {
          // handle error
          console.error(error);
        });
};

  return (
    <div>
      <button onClick={handleClick}>Click</button>
      <button onClick={handleLogout}>logout</button>
      {/* Show the LoginForm if isShown is true */}
      {isShown && <LoginForm />}
    </div>
  );
}

export default App;
