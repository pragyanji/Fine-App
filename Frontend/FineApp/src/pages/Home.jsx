import { useState } from 'react';
import '../css/Home.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function Home() {
  const [formData, setFormData] = useState({
    numberPlate: '',
    vehicleType: '',
    vehicleNumber: '',
    vehicleModel: '',
    fineAmount: '',
    explanation: '',
    photoProof: null,
  });

  const [photoPreview, setPhotoPreview] = useState(null);
  const [vehicleDetails, setVehicleDetails] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handlePhotoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData((prev) => ({
        ...prev,
        photoProof: file,
      }));
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhotoPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const fetchVehicleDetails = async () => {
    if (!formData.numberPlate.trim()) {
      alert('Please enter a number plate');
      return;
    }

    setLoading(true);
    try {
      // API call to fetch vehicle details based on number plate
      const response = await fetch(
        `${API_BASE_URL}/api/vehicle/details/?number_plate=${formData.numberPlate}`
      );
      const data = await response.json();

      if (response.ok) {
        setVehicleDetails(data);
        setFormData((prev) => ({
          ...prev,
          vehicleType: data.vehicle_type || '',
          vehicleModel: data.vehicle_model || '',
          vehicleNumber: data.vehicle_number || '',
        }));
      } else {
        alert('Vehicle not found. Please enter details manually.');
        setVehicleDetails(null);
      }
    } catch (error) {
      console.error('Error fetching vehicle details:', error);
      alert('Error fetching vehicle details. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (
      !formData.numberPlate ||
      !formData.vehicleType ||
      !formData.fineAmount ||
      !formData.explanation ||
      !formData.photoProof
    ) {
      alert('Please fill in all required fields and upload a photo');
      return;
    }

    const formDataToSend = new FormData();
    formDataToSend.append('number_plate', formData.numberPlate);
    formDataToSend.append('vehicle_type', formData.vehicleType);
    formDataToSend.append('vehicle_number', formData.vehicleNumber);
    formDataToSend.append('vehicle_model', formData.vehicleModel);
    formDataToSend.append('fine_amount', formData.fineAmount);
    formDataToSend.append('explanation', formData.explanation);
    formDataToSend.append('photo_proof', formData.photoProof);

    try {
      const response = await fetch(`${API_BASE_URL}/api/fines/create/`, {
        method: 'POST',
        body: formDataToSend,
      });

      if (response.ok) {
        alert('Fine issued successfully! Notification sent to the violator.');
        // Reset form
        setFormData({
          numberPlate: '',
          vehicleType: '',
          vehicleNumber: '',
          vehicleModel: '',
          fineAmount: '',
          explanation: '',
          photoProof: null,
        });
        setPhotoPreview(null);
        setVehicleDetails(null);
      } else {
        alert('Error submitting fine. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting fine:', error);
      alert('Error submitting fine. Please try again.');
    }
  };

  return (
    <div className="home-container">
      <h1>Police Fine Management System</h1>
      <p className="subtitle">Issue fines online with vehicle proof and details</p>

      <form onSubmit={handleSubmit} className="fine-form">
        {/* Number Plate Section */}
        <div className="form-section">
          <h2>Vehicle Information</h2>

          <div className="form-group">
            <label htmlFor="numberPlate">Number Plate *</label>
            <div className="number-plate-input">
              <input
                type="text"
                id="numberPlate"
                name="numberPlate"
                value={formData.numberPlate}
                onChange={handleInputChange}
                placeholder="e.g., BA 1234 AB"
                required
              />
              <button
                type="button"
                onClick={fetchVehicleDetails}
                disabled={loading}
                className="fetch-btn"
              >
                {loading ? 'Fetching...' : 'Fetch Details'}
              </button>
            </div>
            <small>Enter the vehicle's registration number plate</small>
          </div>

          {vehicleDetails && (
            <div className="vehicle-details-info">
              <p>✓ Vehicle found in system</p>
            </div>
          )}

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="vehicleType">Vehicle Type *</label>
              <select
                id="vehicleType"
                name="vehicleType"
                value={formData.vehicleType}
                onChange={handleInputChange}
                required
              >
                <option value="">Select Vehicle Type</option>
                <option value="Motorcycle">Motorcycle</option>
                <option value="Car">Car</option>
                <option value="Bus">Bus</option>
                <option value="Truck">Truck</option>
                <option value="Auto-rickshaw">Auto-rickshaw</option>
                <option value="Scooter">Scooter</option>
                <option value="Taxi">Taxi</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="vehicleNumber">Vehicle Number</label>
              <input
                type="text"
                id="vehicleNumber"
                name="vehicleNumber"
                value={formData.vehicleNumber}
                onChange={handleInputChange}
                placeholder="Auto-filled if found"
                readOnly={vehicleDetails ? true : false}
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="vehicleModel">Vehicle Model</label>
            <input
              type="text"
              id="vehicleModel"
              name="vehicleModel"
              value={formData.vehicleModel}
              onChange={handleInputChange}
              placeholder="Auto-filled if found"
              readOnly={vehicleDetails ? true : false}
            />
          </div>
        </div>

        {/* Proof Section */}
        <div className="form-section">
          <h2>Proof of Violation</h2>

          <div className="form-group">
            <label htmlFor="photoProof">Upload Photo *</label>
            <div className="photo-upload">
              <input
                type="file"
                id="photoProof"
                name="photoProof"
                accept="image/*"
                onChange={handlePhotoUpload}
                required
              />
              <small>Upload a clear photo of the violation as proof</small>
            </div>

            {photoPreview && (
              <div className="photo-preview">
                <img src={photoPreview} alt="Proof preview" />
                <p>Photo selected</p>
              </div>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="explanation">Explanation of Violation *</label>
            <textarea
              id="explanation"
              name="explanation"
              value={formData.explanation}
              onChange={handleInputChange}
              placeholder="Describe the violation in detail (e.g., Jumping red light, Wrong parking, Speeding, etc.)"
              rows="5"
              required
            />
            <small>Provide a clear description of the traffic violation</small>
          </div>
        </div>

        {/* Fine Amount Section */}
        <div className="form-section">
          <h2>Fine Details</h2>

          <div className="form-group">
            <label htmlFor="fineAmount">Fine Amount (₹) *</label>
            <input
              type="number"
              id="fineAmount"
              name="fineAmount"
              value={formData.fineAmount}
              onChange={handleInputChange}
              placeholder="Enter fine amount in rupees"
              min="0"
              required
            />
            <small>Enter the applicable fine amount for this violation</small>
          </div>
        </div>

        {/* Submit Section */}
        <div className="form-section submit-section">
          <button type="submit" className="submit-btn">
            Issue Fine & Send Notification
          </button>
          <p className="submit-info">
            A notification will be sent to the vehicle owner via Nagarik App
          </p>
        </div>
      </form>
    </div>
  );
}

export default Home;
