import React, { useState } from 'react';
import axios from 'axios';

const baseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:10000';
const DB_URL = process.env.REACT_APP_DB_URL || "https://xyz"; 
console.log('Using backend URL:', baseUrl);

const ScrapeForm = () => {
  const [festUrl, setFestUrl] = useState('');
  const [festName, setFestName] = useState('');
  const [college, setCollege] = useState('');
  const [year, setYear] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse('');

    try {
      console.log('POSTing to:', `${baseUrl}/api/scrape`);

      const res = await axios.post(`${baseUrl}/api/scrape`, {
        url: festUrl,
        fest_name: festName,
        college: college,
        year: year,
      });

      setResponse(res.data.message || JSON.stringify(res.data));
    } catch (err) {
      console.error(err);
      setResponse('Error connecting to backend');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundImage: "url('/bg3.jpg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        color: '#fff',
        position: 'relative',
        padding: '1rem',
      }}
    >
      {/* Top-right link (kept as-is) */}
      <div style={{ position: 'absolute', top: 10, right: 20 }}>
        <a
          href={DB_URL}
          target="_blank"
          rel="noopener noreferrer"
          style={{ color: '#0ff', fontSize: '0.9rem' }}
        >
          View Database
        </a>
      </div>

      {/* Centered content */}
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
          padding: '1rem',
        }}
      >
        <h2
          style={{
            marginBottom: '1.5rem',
            textAlign: 'center',
            fontSize: '1.6rem',
          }}
        >
          Scrape Fest Sponsors
        </h2>

        <form
          onSubmit={handleSubmit}
          style={{
            display: 'flex',
            flexDirection: 'column',
            width: '100%',
            maxWidth: '420px',
            gap: '0.75rem',
            background: 'rgba(0, 0, 0, 0.7)',
            padding: '1.5rem',
            borderRadius: '10px',
            boxSizing: 'border-box',
          }}
        >
          <input
            type="text"
            placeholder="Fest URL"
            value={festUrl}
            onChange={(e) => setFestUrl(e.target.value)}
            required
            style={inputStyle}
          />

          <input
            type="text"
            placeholder="Fest Name"
            value={festName}
            onChange={(e) => setFestName(e.target.value)}
            required
            style={inputStyle}
          />

          <input
            type="text"
            placeholder="College Name"
            value={college}
            onChange={(e) => setCollege(e.target.value)}
            required
            style={inputStyle}
          />

          <input
            type="number"
            placeholder="Fest Year"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            required
            style={inputStyle}
          />

          <button
            type="submit"
            disabled={loading}
            style={{
              marginTop: '0.75rem',
              padding: '0.7rem',
              borderRadius: '6px',
              background: '#1e90ff',
              color: '#fff',
              border: 'none',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontSize: '1rem',
            }}
          >
            {loading ? 'Scraping...' : 'Submit'}
          </button>
        </form>
      </div>

      {/* Bottom-center response */}
      {response && (
        <div
          style={{
            position: 'fixed',
            bottom: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'rgba(0,0,0,0.85)',
            padding: '0.8rem 1.2rem',
            borderRadius: '8px',
            maxWidth: '90%',
            textAlign: 'center',
            whiteSpace: 'pre-wrap',
            fontSize: '0.95rem',
          }}
        >
          {response}
        </div>
      )}
    </div>
  );
};

/* Shared input styling */
const inputStyle = {
  padding: '0.65rem',
  borderRadius: '6px',
  border: 'none',
  fontSize: '1rem',
  width: '100%',
  boxSizing: 'border-box',
};

export default ScrapeForm;
