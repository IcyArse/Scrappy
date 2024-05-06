import React, { useState } from 'react';
import axios from 'axios';
import logo from './logo.png'; // Import your logo image
import './LoginForm.css'; // Import CSS file for styling

const LoginForm = () => {
    const [formData, setFormData] = useState({
        email: '',
        classId: '',
        submissionId: ''
    });

    const [message, setMessage] = useState('');
    const [message1, setMessage1] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Remove the first message
        setMessage1('');
    
        try {
            const response = await axios.post('http://localhost:5000/api/submit-data', formData);
            console.log(response.data); // Log server response
    
            // Reset form after successful submission
            setFormData({
                email: '',
                classId: '',
                submissionId: ''
            });

            // Set message to display on the webpage
            setMessage('Give us a moment, retriving your file.');
    
            // Trigger file download after successful submission
            try {
                const downloadResponse = await axios.get('http://localhost:5000/api/download-file', {
                    params: {
                        submissionId: response.data.submission_Id // Assuming response.data contains submissionId
                    },
                    responseType: 'blob', // Important for downloading files
                });

                // Log response headers
                console.log('Response Headers:', downloadResponse.headers);

                // Create a blob object from the response data
                const blob = new Blob([downloadResponse.data], { type: 'application/pdf' });

                // Create a temporary anchor element
                const a = document.createElement('a');
                a.href = window.URL.createObjectURL(blob);
                a.download = formData.filename; // Use filename from form data

                // Simulate a click on the anchor element to trigger the download
                document.body.appendChild(a);
                a.click();

                // Clean up: remove the anchor element
                document.body.removeChild(a);

                // Remove the first message
                setMessage(null);


                // Set message to display on the webpage
                setMessage1('Data retrieved successfully!');

            } catch (error) {
                console.error('Error downloading file:', error);

                // Fetch error message from error.json
                try {
                    const errorResponse = await axios.get('http://localhost:5000/api/error');
                    console.log(errorResponse.data); // Log error response

                    const jsonData = JSON.parse(errorResponse.data);

                    // Set error message
                    setMessage(jsonData.download_error);

                } catch (error) {
                    console.error('Error fetching error message:', error);
                }
            }
        } catch (error) {
            console.error('Error sending data:', error);
        }
    };
    

    return (
        <div className="container">
            <form id="login-form" onSubmit={handleSubmit}>
                <div className="logo">
                    <img src={logo} alt="Logo" className="logo-img" /> {/* Display the logo */}
                </div>
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
                <button type="submit">Retrieve</button>
            </form>
            {message && <p>{message}</p>} {/* Display message if it exists */}
            {message1 && <p>Your file should be downloaded! If not, please try again.</p>} {/* Display message if it exists */}
        </div>
    );
};

export default LoginForm;