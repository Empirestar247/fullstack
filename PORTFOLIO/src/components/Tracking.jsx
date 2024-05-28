import React, { useState } from "react";
import axios from "axios";

function TrackingForm({ onTrack }) {
  const [trackingId, setTrackingId] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    setTrackingId(e.target.value);
    setError(""); // Clear error on new input
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!trackingId.trim()) {
      setError("Please enter a valid Tracking ID.");
      return;
    } else if (trackingId.trim().length !== 8) {
      setError("Tracking ID must be exactly 8 characters long.");
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.get(
        `http://localhost:8000/apptracker/tracking/${ trackingId }`,
      );
      console.log ("response.data", response.data)
      onTrack(response.data);
      setError(""); // Clear errors upon successful data fetching
    } catch (error) {
      console.error(error);
      if (error.response) {
        setError(error.response.data.message);
      } else {
        setError("An error occurred. Please try again later.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Enter your Tracking ID Here"
        className="form-control mt-3 mb-3"
        value={trackingId}
        onChange={handleInputChange}
      />
      {error && <div className="text-danger">{error}</div>}
      <button type="submit" className="btn btn-danger" disabled={isLoading}>
        {isLoading ? "Loading..." : "Track"}
      </button>
    </form>
  );
}

function Tracking() {
  const [tracking, setTracking] = useState(null);

  return (
    <>
      <div className="bg-cover">
        <div className="text-center pt-3 text-light">
          <h2 className="pt-5">Tracking</h2>
          <p>
            Home <i className="fa fa-arrow-right ms-3 me-3"></i> Tracking
          </p>
        </div>
      </div>
      <div className="container mt-5 mb-3">
        <div className="row">
          <div className="col-md-6" data-aos="fade-up">
            <h2>TRACK YOUR SHIPMENT</h2>
            <div className="bg-red"></div>
            <p>
              If you require maximum visibility to your Freight transactions,
              contact our logistic customer team or you can track your cargo by
              using below tracking system.
            </p>
          </div>
          <div className="col-md-6" data-aos="fade-up">
            <TrackingForm onTrack={setTracking} />
            {tracking && (
              <div>
                <h3>Tracking Information:</h3>
                <p>Status: {tracking.status}</p>
                <p>Location: {tracking.location}</p>
                <p>Expected Delivery: {tracking.expectedDelivery}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

export default Tracking;