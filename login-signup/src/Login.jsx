import React, { useState } from "react";

const Login = (props) => {
    const [username, setUsername] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Send POST request to Flask back-end to retrieve login information
        const loginResponse = await fetch('http://localhost:5000/retrieve_mylogin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username
            })
        });
    
        if (loginResponse.ok) {
            const loginData = await loginResponse.json();
            const email = loginData.email;
            const password = loginData.password;
    
            const assignmentsResponse = await fetch('http://localhost:5000/assignments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });
    
            if (assignmentsResponse.ok) {
                const assignmentsData = await assignmentsResponse.json();
                props.setAssignments(assignmentsData);
                props.onLogin();
            } else {
                console.error('Error fetching assignments:', assignmentsResponse.statusText);
            }
        } else {
            console.error('Error fetching login information:', loginResponse.statusText);
        }
    };
    

    return (
        <div className="auth-form-container">
            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="username">Username</label>
                <input
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    type="text"
                    placeholder="johndoe"
                    id="username"
                    name="username"
                />

                <button className="sublog" type="submit">Log In</button>
            </form>
            <button className="link-btn" onClick={() => props.onFormSwitch('register')}>
                Don't have an account? Register here.
            </button>
        </div>
    );
}

export default Login;
