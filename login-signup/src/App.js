import React, { useState } from "react";
import './App.css';
import Login from "./Login";
import Register from "./Register";
import HomePage from "./Homepage"; // Import your HomePage component

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentForm, setCurrentForm] = useState('login');
  const [assignments, setAssignments] = useState([]); 

  const toggleForm = (formName) => {
    setCurrentForm(formName);
  }

  const handleLogin = () => {
    setIsLoggedIn(true); // Set isLoggedIn to true upon successful login
  }

  return (
    <div className="App">
      {isLoggedIn ? (
        <HomePage assignments={assignments} /> 
      ) : (
        currentForm === "login" ? (
          <Login 
            onFormSwitch={toggleForm} 
            onLogin={handleLogin} 
            setAssignments={setAssignments}
          />
        ) : (
          <Register onFormSwitch={toggleForm} />
        )
      )}
    </div>
  );
}

export default App;
