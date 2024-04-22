import React, { useState } from 'react';
import axios from 'axios';

const LoginForm = () => {
    const [formData, setFormData] = useState({
        email: '',
        classId: '',
        submissionId: ''
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://localhost:5000/api/submit-data', formData);
            console.log(response.data); // Log server response
        } catch (error) {
            console.error('Error sending data:', error);
        }

        // Reset form after submission (optional)
        setFormData({
            email: '',
            classId: '',
            submissionId: ''
        });
    };

    return (
        <div className="container">
            <form id="login-form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <input
                        type="text"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="submission-id">Submission ID:</label>
                    <input
                        type="text"
                        id="submission-id"
                        name="submissionId"
                        value={formData.submissionId}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default LoginForm;