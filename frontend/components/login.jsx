import React, { useState } from 'react';
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import axios from "axios";

export function LoginForm() {
    const [isShown, setIsShown] = useState(true);
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevState) => ({ ...prevState, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const formDataToSend = new FormData();
            formDataToSend.append('email', formData.email);
            formDataToSend.append('password', formData.password);

            const response = await axios.post('http://localhost:5000/login', formDataToSend, { withCredentials: true });
            console.log('Form data submitted successfully:', response.data);
            // Aquí podrías redirigir al usuario a otra página o mostrar un mensaje de éxito
        } catch (error) {
            console.error('Error submitting form data:', error);
            if (error.response) {
                console.error('Response data:', error.response.data);
                // Aquí podrías mostrar un mensaje de error específico en tu interfaz de usuario
            } else if (error.request) {
                console.error('Request made but no response received:', error.request);
                // Aquí podrías manejar errores relacionados con la solicitud
            } else {
                console.error('Error setting up the request:', error.message);
                // Aquí podrías manejar otros tipos de errores
            }
        }
    };

    const handleClick = () => {
        setIsShown(false); // Oculta el formulario al hacer clic en "Close"
    };
    return (
        <>
            {isShown && (
                <Card className="w-full max-w-sm">
                    <CardHeader>
                        <CardTitle className="text-2xl">Login</CardTitle>
                        <CardDescription>
                            Enter your email below to login to your account.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="grid gap-4">
                        <div className="grid gap-2">
                            <Label htmlFor="email">Email</Label>
                            <Input name="email" value={formData.email} onChange={handleChange} type="email" required />
                        </div>
                        <div className="grid gap-2">
                            <Label htmlFor="password">Password</Label>
                            <Input name="password" value={formData.password} onChange={handleChange} type="password" required />
                        </div>
                    </CardContent>
                    <CardFooter>
                        <Button onClick={handleSubmit} className="w-full">Sign in</Button>
                    </CardFooter>
                    <CardFooter>
                        <Button onClick={handleClick} className="w-full">Close</Button>
                    </CardFooter>
                </Card>
            )}
        </>
    );
}
