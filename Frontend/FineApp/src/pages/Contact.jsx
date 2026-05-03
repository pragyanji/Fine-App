import { useState } from 'react';
import '../css/Contact.css';

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Here you would typically send the form data to your backend
    console.log('Form submitted:', formData);
    
    // Show success message
    setSubmitted(true);
    
    // Reset form
    setFormData({
      name: '',
      email: '',
      subject: '',
      message: ''
    });

    // Hide success message after 3 seconds
    setTimeout(() => setSubmitted(false), 3000);
  };

  return (
    <div className="contact-container">
      <div className="contact-wrapper">
        <h1 className="contact-title">Contact Us</h1>
        <p className="contact-subtitle">Have a question? We'd love to hear from you.</p>

        {submitted && (
          <div className="success-message">
            Thank you for your message! We'll get back to you soon.
          </div>
        )}

        <form className="contact-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name" className="form-label">Full Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="form-input"
              placeholder="Enter your full name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="email" className="form-label">Email Address *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="form-input"
              placeholder="Enter your email address"
            />
          </div>

          <div className="form-group">
            <label htmlFor="subject" className="form-label">Subject *</label>
            <input
              type="text"
              id="subject"
              name="subject"
              value={formData.subject}
              onChange={handleChange}
              required
              className="form-input"
              placeholder="What is this regarding?"
            />
          </div>

          <div className="form-group">
            <label htmlFor="message" className="form-label">Message *</label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              required
              className="form-textarea"
              placeholder="Enter your message here..."
              rows="6"
            ></textarea>
          </div>

          <button type="submit" className="submit-button">Send Message</button>
        </form>

        <div className="contact-info">
          <div className="info-item">
            <h3>Email</h3>
            <p>info@fineapp.com</p>
          </div>
          <div className="info-item">
            <h3>Phone</h3>
            <p>+1 (555) 123-4567</p>
          </div>
          <div className="info-item">
            <h3>Address</h3>
            <p>123 Main Street, City, State 12345</p>
          </div>
        </div>
      </div>
    </div>
  );
}