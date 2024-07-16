import Link from "next/link"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
axios.defaults.withCredentials = true;

function App() {
    // usestate for setting a javascript
    // object for storing and using data
    const [data, setdata] = useState({
        name: "",
        age: 0,
        programming: "",
    });

    // Using useEffect for single rendering
    useEffect(() => {
        // Using axios to fetch the api from 
        // flask server it will be redirected to proxy
        axios.get("http://localhost:5000//data")
            .then((response) => {
                // Setting a data from api
                setdata({
                    name: response.data.Name,
                    age: response.data.Age,
                    programming: response.data.programming,
                });
            })
            .catch((error) => {
                console.error("There was an error fetching the data!", error);
            });
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <h1>React and Flask</h1>
                {/* Calling a data from setdata for showing */}
                <p>{data.name}</p>
                <p>{data.age}</p>
                <p>{data.programming}</p>
            </header>
        </div>
    );
}

export default App;